# encoding: utf-8
# Copyright (C) 2015 John Törnblom

from tests.test_bridgepoint.utils import PrebuildFunctionTestCase
from tests.test_bridgepoint.utils import prebuild_docstring

from xtuml import navigate_one as one


class TestBinOp(PrebuildFunctionTestCase):

    @prebuild_docstring
    def test_plus(self):
        '''return 1 + 1;'''
        act_ret = self.metamodel.select_one('ACT_RET')
        self.assertIsNotNone(act_ret)
        
        act_smt = one(act_ret).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ret).V_VAL[668]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.startPosition, 8)
        self.assertEqual(v_val.endPosition, 12)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'integer')
        
        v_bin = one(v_val).V_BIN[801]()
        self.assertEqual(v_bin.Operator, '+')
        
        v_val = one(v_bin).V_VAL[802]()
        self.assertIsNotNone(v_val)
        
        v_val = one(v_bin).V_VAL[803]()
        self.assertIsNotNone(v_val)        
        
    @prebuild_docstring
    def test_grouped_binop(self):
        '''return (1 + 1);'''
        act_ret = self.metamodel.select_one('ACT_RET')
        self.assertIsNotNone(act_ret)
        
        act_smt = one(act_ret).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ret).V_VAL[668]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.startPosition, 8)
        self.assertEqual(v_val.endPosition, 14)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'integer')
        
        v_bin = one(v_val).V_BIN[801]()
        self.assertEqual(v_bin.Operator, '+')
        
        v_val = one(v_bin).V_VAL[802]()
        self.assertIsNotNone(v_val)
        
        v_val = one(v_bin).V_VAL[803]()
        self.assertIsNotNone(v_val)
    
    @prebuild_docstring
    def test_minus(self):
        '''return 1 - 1;'''
        act_ret = self.metamodel.select_one('ACT_RET')
        self.assertIsNotNone(act_ret)
        
        act_smt = one(act_ret).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ret).V_VAL[668]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.startPosition, 8)
        self.assertEqual(v_val.endPosition, 12)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'integer')
        
        v_bin = one(v_val).V_BIN[801]()
        self.assertEqual(v_bin.Operator, '-')
        
        v_val = one(v_bin).V_VAL[802]()
        self.assertIsNotNone(v_val)
        
        v_val = one(v_bin).V_VAL[803]()
        self.assertIsNotNone(v_val)

    @prebuild_docstring
    def test_unary_minus(self):
        '''return 1 - -1;'''
        act_ret = self.metamodel.select_one('ACT_RET')
        self.assertIsNotNone(act_ret)
        
        act_smt = one(act_ret).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ret).V_VAL[668]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.startPosition, 8)
        self.assertEqual(v_val.endPosition, 13)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'integer')
        
        v_bin = one(v_val).V_BIN[801]()
        self.assertEqual(v_bin.Operator, '-')
        
        v_val = one(v_bin).V_VAL[802]()
        self.assertIsNotNone(v_val)
        
        v_uny = one(v_bin).V_VAL[803].V_UNY[801]()
        self.assertEqual(v_uny.Operator, '-')
        
    @prebuild_docstring
    def test_real_mult(self):
        '''return 2.0 * 2.0;'''
        act_ret = self.metamodel.select_one('ACT_RET')
        self.assertIsNotNone(act_ret)
        
        act_smt = one(act_ret).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ret).V_VAL[668]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.startPosition, 8)
        self.assertEqual(v_val.endPosition, 16)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'real')
        
        v_bin = one(v_val).V_BIN[801]()
        self.assertEqual(v_bin.Operator, '*')
        
        v_val = one(v_bin).V_VAL[802]()
        self.assertIsNotNone(v_val)
        
        v_val = one(v_bin).V_VAL[803]()
        self.assertIsNotNone(v_val)
        
    @prebuild_docstring
    def test_integer_div(self):
        '''return 5 / 2;'''
        act_ret = self.metamodel.select_one('ACT_RET')
        self.assertIsNotNone(act_ret)
        
        act_smt = one(act_ret).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ret).V_VAL[668]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.startPosition, 8)
        self.assertEqual(v_val.endPosition, 12)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'integer')
        
        v_bin = one(v_val).V_BIN[801]()
        self.assertEqual(v_bin.Operator, '/')
        
        v_val = one(v_bin).V_VAL[802]()
        self.assertIsNotNone(v_val)
        
        v_val = one(v_bin).V_VAL[803]()
        self.assertIsNotNone(v_val)
        
    @prebuild_docstring
    def test_less_true(self):
        '''return 0 < 1;'''
        act_ret = self.metamodel.select_one('ACT_RET')
        self.assertIsNotNone(act_ret)
        
        act_smt = one(act_ret).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ret).V_VAL[668]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.startPosition, 8)
        self.assertEqual(v_val.endPosition, 12)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'boolean')
        
        v_bin = one(v_val).V_BIN[801]()
        self.assertEqual(v_bin.Operator, '<')
        
        v_val = one(v_bin).V_VAL[802]()
        self.assertIsNotNone(v_val)
        
        v_val = one(v_bin).V_VAL[803]()
        self.assertIsNotNone(v_val)
        
    @prebuild_docstring
    def test_less_eq_true(self):
        '''return 1 <= 1;'''
        act_ret = self.metamodel.select_one('ACT_RET')
        self.assertIsNotNone(act_ret)
        
        act_smt = one(act_ret).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ret).V_VAL[668]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.startPosition, 8)
        self.assertEqual(v_val.endPosition, 13)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'boolean')
        
        v_bin = one(v_val).V_BIN[801]()
        self.assertEqual(v_bin.Operator, '<=')
        
        v_val = one(v_bin).V_VAL[802]()
        self.assertIsNotNone(v_val)
        
        v_val = one(v_bin).V_VAL[803]()
        self.assertIsNotNone(v_val)

    @prebuild_docstring
    def test_chained_binop_1(self):
        '''return (1 + 1) - 1;'''
        act_ret = self.metamodel.select_one('ACT_RET')
        self.assertIsNotNone(act_ret)
        
        act_smt = one(act_ret).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ret).V_VAL[668]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.startPosition, 8)
        self.assertEqual(v_val.endPosition, 18)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'integer')
        
        v_bin = one(v_val).V_BIN[801]()
        self.assertEqual(v_bin.Operator, '-')
        
        v_val = one(v_bin).V_VAL[802]()
        self.assertIsNotNone(v_val)
        
        v_val = one(v_bin).V_VAL[803]()
        self.assertIsNotNone(v_val)

    @prebuild_docstring
    def test_chained_binop_2(self):
        '''return 1 + (1 - 1);'''
        act_ret = self.metamodel.select_one('ACT_RET')
        self.assertIsNotNone(act_ret)
        
        act_smt = one(act_ret).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ret).V_VAL[668]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.startPosition, 8)
        self.assertEqual(v_val.endPosition, 18)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'integer')
        
        v_bin = one(v_val).V_BIN[801]()
        self.assertEqual(v_bin.Operator, '+')
        
        v_val = one(v_bin).V_VAL[802]()
        self.assertIsNotNone(v_val)
        
        v_val = one(v_bin).V_VAL[803]()
        self.assertIsNotNone(v_val)
        
    @prebuild_docstring
    def test_chained_unary_op(self):
        '''return not (1 == 1);'''
        act_ret = self.metamodel.select_one('ACT_RET')
        self.assertIsNotNone(act_ret)
        
        act_smt = one(act_ret).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ret).V_VAL[668]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.startPosition, 8)
        self.assertEqual(v_val.endPosition, 19)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'boolean')
        
        v_uny = one(v_val).V_UNY[801]()
        self.assertEqual(v_uny.Operator, 'not')
        
        v_val = one(v_uny).V_VAL[804]()
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'boolean')
        
        v_bin = one(v_val).V_BIN[801]()
        self.assertEqual(v_bin.Operator, '==')
        
        v_val = one(v_bin).V_VAL[802]()
        self.assertIsNotNone(v_val)
        
        v_val = one(v_bin).V_VAL[803]()
        self.assertIsNotNone(v_val)

    @prebuild_docstring
    def test_and_binop_true(self):
        '''return True and True;'''
        act_ret = self.metamodel.select_one('ACT_RET')
        self.assertIsNotNone(act_ret)
        
        act_smt = one(act_ret).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ret).V_VAL[668]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.startPosition, 8)
        self.assertEqual(v_val.endPosition, 20)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'boolean')
        
        v_bin = one(v_val).V_BIN[801]()
        self.assertEqual(v_bin.Operator, 'and')
        
        v_val = one(v_bin).V_VAL[802]()
        self.assertIsNotNone(v_val)
        
        v_val = one(v_bin).V_VAL[803]()
        self.assertIsNotNone(v_val)
        
    @prebuild_docstring
    def test_or_binop_true(self):
        '''return True or False;'''
        act_ret = self.metamodel.select_one('ACT_RET')
        self.assertIsNotNone(act_ret)
        
        act_smt = one(act_ret).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ret).V_VAL[668]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.startPosition, 8)
        self.assertEqual(v_val.endPosition, 20)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'boolean')
        
        v_bin = one(v_val).V_BIN[801]()
        self.assertEqual(v_bin.Operator, 'or')
        
        v_val = one(v_bin).V_VAL[802]()
        self.assertIsNotNone(v_val)
        
        v_val = one(v_bin).V_VAL[803]()
        self.assertIsNotNone(v_val)
        
    
if __name__ == "__main__":
    import logging
    import unittest
    
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
    
