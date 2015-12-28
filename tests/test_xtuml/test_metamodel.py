# encoding: utf-8
# Copyright (C) 2014-2015 John Törnblom

import unittest

import xtuml
from bridgepoint import ooaofooa
from xtuml import where_eq as where

from tests.test_xtuml.utils import expect_exception


class TestAssociation(unittest.TestCase):
    '''
    Test suite for the class xtuml.AssociationLink
    '''
    
    def testAssociationConstructor(self):
        l1 = xtuml.AssociationLink('CLASS1', '1C', [], 'next')
        l2 = xtuml.AssociationLink('CLASS1', '1C', [], 'prev')
        ass = xtuml.Association(1, l1, l2)
        self.assertEqual(ass.id, 'R1')
        self.assertTrue(ass.is_reflexive)

        l1 = xtuml.AssociationLink('CLASS1', '1C', [], 'next')
        l2 = xtuml.AssociationLink('CLASS2', '1C', [], 'prev')
        ass = xtuml.Association('R2', l1, l2)
        self.assertEqual(ass.id, 'R2')
        self.assertFalse(ass.is_reflexive)
        
    def testAssociationLinkConstructor(self):
        l = xtuml.AssociationLink('CLASS', '1', [], 'test')
        self.assertFalse(l.is_many)
        self.assertFalse(l.is_conditional)

        l = xtuml.AssociationLink('CLASS', '1C', [], 'test')
        self.assertFalse(l.is_many)
        self.assertTrue(l.is_conditional)

        l = xtuml.AssociationLink('CLASS', '1c', [], 'test')
        self.assertFalse(l.is_many)
        self.assertTrue(l.is_conditional)

        l = xtuml.AssociationLink('CLASS', 'MC', [], 'test')
        self.assertTrue(l.is_many)
        self.assertTrue(l.is_conditional)

        l = xtuml.AssociationLink('CLASS', 'mC', [], 'test')
        self.assertTrue(l.is_many)
        self.assertTrue(l.is_conditional)

        l = xtuml.AssociationLink('CLASS', 'Mc', [], 'test')
        self.assertTrue(l.is_many)
        self.assertTrue(l.is_conditional)

        l = xtuml.AssociationLink('CLASS', 'mc', [], 'test')
        self.assertTrue(l.is_many)
        self.assertTrue(l.is_conditional)
        
        
class TestNavChain(unittest.TestCase):
    '''
    Test suite for the class xtuml.NavChain
    '''
    
    def testNavigateNone(self):
        self.assertIsNone(xtuml.navigate_one(None)())
        self.assertEqual(len(xtuml.navigate_many(None)()), 0)

    @expect_exception(xtuml.ModelException)
    def testNavigateInvalidHandle(self):
        self.assertIsNone(xtuml.navigate_one('test')())

        
class TestModel(unittest.TestCase):
    '''
    Test suite for the class xtuml.MetaModel
    '''
    
    @classmethod
    def setUpClass(cls):
        cls.loader = ooaofooa.Loader()
 
    def setUp(self):
        self.metamodel = self.loader.build_metamodel()

    def tearDown(self):
        del self.metamodel

    def testSelectAny(self):
        m = self.metamodel
        self.assertNotEqual(m.select_any('S_DT'), None)

    def testSelectOne(self):
        m = self.metamodel
        self.assertNotEqual(m.select_one('S_DT'), None)
        
    def testSelectMany(self):
        m = self.metamodel
        q = m.select_many('S_DT')
        self.assertIsInstance(q, xtuml.QuerySet)
        self.assertTrue(len(q) > 0)
        
        q = m.select_many('S_EDT')
        self.assertIsInstance(q, xtuml.QuerySet)
        self.assertTrue(len(q) == 0)
        
    def testSelectAnyWhere(self):
        m = self.metamodel
        inst = m.select_any('S_DT', where(Name='void'))
        self.assertEqual(inst.Name, 'void')
        
    def testNavOne(self):
        m = self.metamodel
        s_dt = m.select_any('S_DT',  where(Name='void'))
        pe_pe = xtuml.navigate_one(s_dt).PE_PE[8001](lambda inst: True)
        self.assertEqual(s_dt.DT_ID, pe_pe.Element_ID)
        
    def testNavMany(self):
        m = self.metamodel
        s_dt = m.select_many('S_DT')
        pe_pe = xtuml.navigate_many(s_dt).PE_PE[8001](lambda inst: True)
        self.assertEqual(len(s_dt), len(pe_pe))
   
    def testNavSubtype(self):
        m = self.metamodel
        s_dt = m.select_any('S_DT',  where(Name='void'))
        s_cdt = xtuml.navigate_subtype(s_dt, 17)
        self.assertTrue(s_cdt)
        self.assertEqual(s_cdt.__class__.__name__, 'S_CDT')
        
    def testEmpty(self):
        m = self.metamodel
        self.assertTrue(len(m.select_many('S_DT', lambda inst: False)) == 0)
        self.assertFalse(len(m.select_many('S_DT')) == 0)
       
    def testCardinality(self):
        m = self.metamodel
        
        q = m.select_many('S_DT', lambda inst: False)
        self.assertEqual(0, len(q))
        
        q = m.select_many('S_DT')
        self.assertTrue(len(q) > 0)
        
        x = 0
        for _ in q:
            x += 1
            
        self.assertEqual(x, len(q))
        
    def testIsSet(self):
        m = self.metamodel

        q = m.select_many('S_DT', lambda inst: False)
        self.assertIsInstance(q, xtuml.QuerySet)
        
        q = m.select_many('S_DT')
        self.assertIsInstance(q, xtuml.QuerySet)
                
    def testIsInstance(self):
        m = self.metamodel
        
        q = m.select_any('S_DT')
        self.assertIsInstance(q, xtuml.BaseObject)

    def testQueryOrder(self):
        m = self.metamodel
        q = m.select_many('S_DT')
        
        length = len(q)
        for index, inst in enumerate(q):
            self.assertEqual(index == 0, inst == q.first)
            self.assertEqual(index != 0, inst != q.first)
            self.assertEqual(index == length - 1, inst == q.last)
            self.assertEqual(index != length - 1, inst != q.last)

    def testCaseSensitivity(self):
        self.metamodel.define_class('Aa', [])
        
        self.metamodel.new('AA')

        self.assertTrue(self.metamodel.select_any('aA'))
        self.assertTrue(self.metamodel.select_any('AA'))
        self.assertTrue(self.metamodel.select_any('Aa'))
        self.assertTrue(self.metamodel.select_any('aa'))

        self.metamodel.new('Aa')
        self.metamodel.new('aA')
        self.metamodel.new('aa')
        
        self.assertEqual(len(self.metamodel.select_many('aA')), 4)
        self.assertEqual(len(self.metamodel.select_many('AA')), 4)
        self.assertEqual(len(self.metamodel.select_many('Aa')), 4)
        self.assertEqual(len(self.metamodel.select_many('aa')), 4)
        
    @expect_exception(xtuml.ModelException)
    def testUnknownType(self):
        self.metamodel.define_class('A', [('Id', '<invalid type>')])
        self.metamodel.new('A')
        
    @expect_exception(xtuml.ModelException)
    def testUndefinedClass(self):
        self.metamodel.new('MY_UNDEFINED_CLASS')

    @expect_exception(xtuml.ModelException)
    def testRedefinedClass1(self):
        self.metamodel.define_class('MY_CLASS', [])
        self.metamodel.define_class('MY_CLASS', [])

    @expect_exception(xtuml.ModelException)
    def testSelectAnyUndefined(self):
        self.metamodel.select_any('MY_CLASS')

    @expect_exception(xtuml.ModelException)
    def testSelectManyUndefined(self):
        self.metamodel.select_many('MY_CLASS')
        
    def testRelate(self):
        s_edt = self.metamodel.new('S_EDT')
        s_dt = self.metamodel.new('S_DT')
        pe_pe = self.metamodel.new('PE_PE')
        self.assertTrue(xtuml.relate(s_dt, pe_pe, 8001))
        self.assertTrue(xtuml.relate(s_dt, s_edt, 17))
        self.assertEqual(s_edt, xtuml.navigate_one(s_dt).S_EDT[17]())

    def testDelete(self):
        inst = self.metamodel.select_any('S_DT', where(Name='void'))
        xtuml.delete(inst)
        
        inst = self.metamodel.select_any('S_DT', where(Name='void'))
        self.assertFalse(inst)
    
    @expect_exception(xtuml.ModelException)
    def testDeleteRwise(self):
        inst = self.metamodel.select_any('S_DT', where(Name='void'))
        xtuml.delete(inst)
        xtuml.delete(inst)

    def testClone(self):
        s_ee = self.metamodel.new('S_EE', Name='Test', Descrip='test', Key_Lett='TEST')
        pe_pe = self.metamodel.new('PE_PE')
        self.assertTrue(xtuml.relate(s_ee, pe_pe, 8001))
        
        m = ooaofooa.empty_model()
        self.assertNotEqual(pe_pe, m.clone(pe_pe))
        self.assertNotEqual(s_ee, m.clone(s_ee))
        
        s_ee_clone = m.select_any('S_EE', where(Name='Test'))
        self.assertNotEqual(s_ee, s_ee_clone)
        self.assertEqual(s_ee_clone.EE_ID, s_ee.EE_ID)
        self.assertEqual(s_ee_clone.Name, s_ee.Name)
        self.assertEqual(s_ee_clone.Descrip, s_ee.Descrip)
        self.assertEqual(s_ee_clone.Key_Lett, s_ee.Key_Lett)
        

        pe_pe_clone = xtuml.navigate_one(s_ee_clone).PE_PE[8001]()
        self.assertTrue(pe_pe_clone)
        self.assertNotEqual(pe_pe, pe_pe_clone)
        self.assertEqual(pe_pe_clone.Element_ID, pe_pe.Element_ID)
        self.assertEqual(pe_pe_clone.Visibility, pe_pe.Visibility)
        self.assertEqual(pe_pe_clone.Package_ID, pe_pe.Package_ID)
        self.assertEqual(pe_pe_clone.Component_ID, pe_pe.Component_ID)
        self.assertEqual(pe_pe_clone.type, pe_pe.type)
        
    @expect_exception(xtuml.ModelException)
    def testDeleteUnknownInstance(self):
        xtuml.delete(self)
        
    def testRelateReflexive1(self):
        inst1 = self.metamodel.new('ACT_SMT')
        inst2 = self.metamodel.new('ACT_SMT')
        act_blk = self.metamodel.new('ACT_BLK')

        self.assertTrue(xtuml.relate(inst1, act_blk, 602))
        self.assertTrue(xtuml.relate(inst2, act_blk, 602))
        self.assertTrue(xtuml.relate(inst1, inst2, 661, 'precedes'))
        self.assertEqual(inst2, xtuml.navigate_one(inst1).ACT_SMT[661, 'succeeds']())
        self.assertEqual(inst1, xtuml.navigate_one(inst2).ACT_SMT[661, 'precedes']())
        
    def testRelateReflexive2(self):
        inst1 = self.metamodel.new('ACT_SMT')
        inst2 = self.metamodel.new('ACT_SMT')
        act_blk = self.metamodel.new('ACT_BLK')

        self.assertTrue(xtuml.relate(inst1, act_blk, 602))
        self.assertTrue(xtuml.relate(inst2, act_blk, 602))
        self.assertTrue(xtuml.relate(inst2, inst1, 661, 'succeeds'))
        self.assertEqual(inst2, xtuml.navigate_one(inst1).ACT_SMT[661, 'succeeds']())
        self.assertEqual(inst1, xtuml.navigate_one(inst2).ACT_SMT[661, 'precedes']())
        
    @expect_exception(xtuml.ModelException)
    def testRelateReflexiveWithoutPhrase(self):
        inst1 = self.metamodel.new('ACT_SMT')
        inst2 = self.metamodel.new('ACT_SMT')
        
        xtuml.relate(inst1, inst2, 661, '<invalid phrase>')
        
    def testRelateInvertedOrder(self):
        s_edt = self.metamodel.new('S_EDT')
        s_dt = self.metamodel.new('S_DT')
        pe_pe = self.metamodel.new('PE_PE')
        self.assertTrue(xtuml.relate(pe_pe, s_dt, 8001))
        self.assertTrue(xtuml.relate(s_edt, s_dt, 17))
        self.assertEqual(s_edt, xtuml.navigate_one(s_dt).S_EDT[17]())
    
    @expect_exception(xtuml.ModelException)
    def testRelateInvalidRelId(self):
        s_edt = self.metamodel.new('S_EDT')
        s_dt = self.metamodel.new('S_DT')
        xtuml.relate(s_edt, s_dt, 0)
        self.assertEqual(s_edt, xtuml.navigate_one(s_dt).S_EDT[17]())
        
    def testUnrelate(self):
        inst1 = self.metamodel.new('ACT_SMT')
        inst2 = self.metamodel.new('ACT_SMT')
        act_blk = self.metamodel.new('ACT_BLK')

        self.assertTrue(xtuml.relate(inst1, act_blk, 602))
        self.assertTrue(xtuml.relate(inst2, act_blk, 602))
        
        self.assertTrue(xtuml.relate(inst1, inst2, 661, 'precedes'))
        self.assertEqual(inst2, xtuml.navigate_one(inst1).ACT_SMT[661, 'succeeds']())
        self.assertEqual(inst1, xtuml.navigate_one(inst2).ACT_SMT[661, 'precedes']())
        
        self.assertTrue(xtuml.unrelate(inst1, inst2, 661, 'precedes'))
        self.assertIsNone(xtuml.navigate_one(inst2).ACT_SMT[661, 'precedes']())
        self.assertIsNone(xtuml.navigate_one(inst1).ACT_SMT[661, 'succeeds']())
            
    def testRelateInWrongOrder(self):
        s_ee = self.metamodel.new('S_EE')
        pe_pe = self.metamodel.new('PE_PE')
        EE_ID = s_ee.EE_ID
        Element_ID = pe_pe.Element_ID
        self.assertTrue(xtuml.relate(s_ee, pe_pe, 8001))
        self.assertNotEqual(EE_ID, s_ee.EE_ID)
        self.assertEqual(Element_ID, pe_pe.Element_ID)

    def testRelateTopDown(self):
        m = self.metamodel
        s_dt = m.select_one('S_DT', where(Name='string'))
        s_bparm = m.new('S_BPARM', Name='My_Parameter')
        s_ee = m.new('S_EE', Name='My_External_Entity', Key_Lett='My_External_Entity')
        pe_pe = m.new('PE_PE', Visibility=True, type=5)
        s_brg = m.new('S_BRG', Name='My_Bridge_Operation')

        self.assertTrue(xtuml.relate(s_ee, pe_pe, 8001))
        self.assertTrue(xtuml.relate(s_brg, s_ee, 19))
        self.assertTrue(xtuml.relate(s_brg, s_dt, 20))
        self.assertTrue(xtuml.relate(s_bparm, s_brg, 21))
        self.assertTrue(xtuml.relate(s_bparm, s_dt, 22))
            
        inst = xtuml.navigate_any(pe_pe).S_EE[8001].S_BRG[19].S_BPARM[21]()
        self.assertEqual(inst, s_bparm)
        
    def testRelateBottomUp(self):
        m = self.metamodel
        s_dt = m.select_one('S_DT', where(Name='string'))
        s_bparm = m.new('S_BPARM', Name='My_Parameter')
        s_ee = m.new('S_EE', Name='My_External_Entity', Key_Lett='My_External_Entity')
        pe_pe = m.new('PE_PE', Visibility=True, type=5)
        s_brg = m.new('S_BRG', Name='My_Bridge_Operation')
        
        self.assertTrue(xtuml.relate(s_bparm, s_dt, 22))
        self.assertTrue(xtuml.relate(s_bparm, s_brg, 21))
        self.assertTrue(xtuml.relate(s_brg, s_dt, 20))
        self.assertTrue(xtuml.relate(s_ee, pe_pe, 8001))
        self.assertTrue(xtuml.relate(s_brg, s_ee, 19))
        
        inst = xtuml.navigate_any(pe_pe).S_EE[8001].S_BRG[19].S_BPARM[21]()
        self.assertEqual(inst, s_bparm)
    
    def testConcistencyOfEmptyModel(self):
        self.assertTrue(self.metamodel.is_consistent())
    
    def testConsistencyOfNonEmptyModel(self):
        m = self.metamodel
        s_dt = m.select_one('S_DT', where(Name='string'))
        s_bparm = m.new('S_BPARM', Name='My_Parameter')
        s_ee = m.new('S_EE', Name='My_External_Entity', Key_Lett='My_External_Entity')
        pe_pe = m.new('PE_PE', Visibility=True, type=5)
        s_brg = m.new('S_BRG', Name='My_Bridge_Operation')
        
        self.assertFalse(m.is_consistent(22))
        self.assertTrue(xtuml.relate(s_bparm, s_dt, 22))
        self.assertTrue(m.is_consistent(22))
        
        self.assertFalse(m.is_consistent(21))
        self.assertTrue(xtuml.relate(s_bparm, s_brg, 21))
        self.assertTrue(m.is_consistent(21))
        
        self.assertFalse(m.is_consistent(20))
        self.assertTrue(xtuml.relate(s_brg, s_dt, 20))
        self.assertTrue(m.is_consistent(20))
        
        self.assertFalse(m.is_consistent(8001))
        self.assertTrue(xtuml.relate(s_ee, pe_pe, 8001))
        self.assertTrue(m.is_consistent(8001))
        
        self.assertFalse(m.is_consistent(19))
        self.assertTrue(xtuml.relate(s_brg, s_ee, 19))
        self.assertTrue(m.is_consistent(19))
        
        # the old, unused association R8 is still present in ooaofooa, and thus
        # consistency check fails on S_EE.
        #self.assertTrue(m.is_consistent())
        
class TestDefineAssociations(unittest.TestCase):
    '''
    Test suite for the tests the class xtuml.MetaModel ability to define associations.
    '''
 
    def setUp(self):
        self.metamodel = xtuml.MetaModel()

    def tearDown(self):
        del self.metamodel

    def testReflexive(self):
        self.metamodel.define_class('A', [('Id', 'unique_id'),
                                          ('Next_Id', 'unique_id'),
                                          ('Name', 'string')])
        
        endpint1 = xtuml.SingleAssociationLink('A', ids=['Id'], phrase='prev')
        endpint2 = xtuml.SingleAssociationLink('A', ids=['Next_Id'], phrase='next')
        self.metamodel.define_relation('R1', endpint1, endpint2)
        
        first = self.metamodel.new('A', Name="First")
        second = self.metamodel.new('A', Name="Second")

        self.assertTrue(xtuml.relate(first, second, 1, 'prev'))

        inst = xtuml.navigate_one(first).A[1, 'next']()
        self.assertEqual(inst.Name, second.Name)

        inst = xtuml.navigate_one(first).A[1, 'prev']()
        self.assertIsNone(inst)
        
        inst = xtuml.navigate_one(second).A[1, 'prev']()
        self.assertEqual(inst.Name, first.Name)
        
        inst = xtuml.navigate_one(second).A[1, 'next']()
        self.assertIsNone(inst)

    def testOneToMany(self):
        self.metamodel.define_class('A', [('Id', 'unique_id')])
        self.metamodel.define_class('B', [('Id', 'unique_id'), ('A_Id', 'unique_id')])
        a_endpint = xtuml.SingleAssociationLink('A', ids=['Id'])
        b_endpint = xtuml.ManyAssociationLink('B', ids=['A_Id'])
        
        self.metamodel.define_relation(1, a_endpint, b_endpint)
        
        a = self.metamodel.new('A')
        b = self.metamodel.new('B')
        self.assertTrue(xtuml.relate(a, b, 1))
        
        self.assertEqual(a, xtuml.navigate_one(b).A[1]())


class TestBaseObject(unittest.TestCase):
    '''
    Test suite for the class xtuml.BaseObject
    '''
    
    def testPlusOperator(self):
        inst1 = xtuml.BaseObject()
        inst2 = xtuml.BaseObject()

        q = inst1 + inst2
        self.assertEqual(2, len(q))
        self.assertIn(inst1, q)
        self.assertIn(inst2, q)
        
    def testMinusOperator(self):
        inst1 = xtuml.BaseObject()
        inst2 = xtuml.BaseObject()

        q = inst1 - inst2
        self.assertEqual(1, len(q))
        self.assertIn(inst1, q)
        self.assertNotIn(inst2, q)
        
    def testNonPersistingAttribute(self):
        inst = xtuml.BaseObject()
        
        setattr(inst, 'test1', 1)
        self.assertEqual(getattr(inst, 'test1'), 1)
        self.assertEqual(inst.test1, 1)
        
        inst.__dict__['test2'] = 2
        self.assertEqual(getattr(inst, 'test2'), 2)
        self.assertEqual(inst.test2, 2)

        inst.test3 = 3
        self.assertEqual(getattr(inst, 'test3'), 3)
        self.assertEqual(inst.test3, 3)
        
    @expect_exception(AttributeError)
    def testUndefinedAttribute1(self):
        inst = xtuml.BaseObject()
        _ = getattr(inst, 'test')
        
        
    @expect_exception(AttributeError)
    def testUndefinedAttribute2(self):
        inst = xtuml.BaseObject()
        _ = inst.test
        
        
class TestQuerySet(unittest.TestCase):
    '''
    Test suite for the class xtuml.QuerySet
    '''
    
    def testEqualOperator(self):
        q1 = xtuml.QuerySet()
        q2 = xtuml.QuerySet()
        
        self.assertEqual(q1, q2)
        
        q1 = xtuml.QuerySet([1])
        q2 = xtuml.QuerySet([1])
        
        self.assertEqual(q1, q2)
        
        q1 = xtuml.QuerySet([1, 2, 3])
        q2 = xtuml.QuerySet([1, 2, 3])
        
        self.assertEqual(q1, q2)
        self.assertEqual(q1, [1, 2, 3])
        
    def testNotEqualOperator(self):
        q1 = xtuml.QuerySet()
        q2 = xtuml.QuerySet([1])
        self.assertNotEqual(q1, q2)
        self.assertNotEqual(q2, q1)
        
        q1 = xtuml.QuerySet([1, 2, 3])
        q2 = xtuml.QuerySet([1, 3])
        self.assertNotEqual(q1, q2)
        self.assertNotEqual(q2, q1)
        
        q1 = xtuml.QuerySet([1, 2, 3])
        q2 = xtuml.QuerySet([1, 3, 2])
        self.assertNotEqual(q1, q2)
        
    @expect_exception(KeyError)
    def testPopEmpty(self):
        q = xtuml.QuerySet()
        q.pop()

    def testPopLast(self):
        q1 = xtuml.QuerySet([1, 2])
        q2 = xtuml.QuerySet([1])
        self.assertNotEqual(q1, q2)

        q1.pop()
        self.assertEqual(q1, q2)
        
    def testPopFirst(self):
        q1 = xtuml.QuerySet([2, 1])
        q2 = xtuml.QuerySet([1])
        self.assertNotEqual(q1, q2)

        q1.pop(last=False)
        self.assertEqual(q1, q2)

class TestIdGenerator(unittest.TestCase):
    '''
    Test suite for the IdGenerator classes
    '''

    def testIntegerGeneratorBasic(self):
        i = xtuml.IntegerGenerator()
        self.assertEqual(i.peek(), 1)
        self.assertEqual(i.next(), 1)
        self.assertEqual(i.next(), 2)
        self.assertEqual(i.peek(), 3)
        self.assertEqual(i.peek(), 3)

    def testIntegerGeneratorIterator(self):
        i = xtuml.IntegerGenerator()
        count = 1
        for v in i:
            self.assertEqual(v, count)
            count += 1
            if count == 10:
                break;


if __name__ == "__main__":
    unittest.main()

