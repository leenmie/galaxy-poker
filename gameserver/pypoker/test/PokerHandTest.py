'''
Created on Apr 16, 2014

@author: leen
'''
import unittest
import random
import pypoker.PokerHand as Hand
from pypoker.helper.poker import get_PokerHand_from_list

class PokerHandTest(unittest.TestCase):
    
    def testPokerHand5CardsGeneric(self):
        for _count in xrange(10000):
            hand1 = get_PokerHand_from_list([random.randint(0,51) for _ in range(5)])
            hand2 = get_PokerHand_from_list([random.randint(0,51) for _ in range(5)])
            
            self.assertTrue(len(hand1.mean_cards)==5)     
            self.assertTrue(len(hand2.mean_cards)==5)            
              
            if hand1 < hand2:
                self.assertLessEqual(hand1.hand, hand2.hand)
            elif hand1 > hand2:
                self.assertGreaterEqual(hand1.hand, hand2.hand)
            elif hand1 == hand2:
                self.assertEqual(hand1.hand, hand2.hand)
    
    def testPokerHand7CardsGeneric(self):
        for _count in xrange(10000):
            hand1 = get_PokerHand_from_list([random.randint(0,51) for _ in range(7)])
            hand2 = get_PokerHand_from_list([random.randint(0,51) for _ in range(7)])
            self.assertTrue(len(hand1.mean_cards)==5)     
            self.assertTrue(len(hand2.mean_cards)==5)   
            if hand1 < hand2:
                self.assertLessEqual(hand1.hand, hand2.hand)
            elif hand1 > hand2:
                self.assertGreaterEqual(hand1.hand, hand2.hand)
            elif hand1 == hand2:
                self.assertEqual(hand1.hand, hand2.hand)    
                
    def testPokerHandHighCard(self):        
        hand1 = get_PokerHand_from_list([1, 9, 18, 25, 35])
        hand2 = get_PokerHand_from_list([2, 10, 19, 26, 34])
        self.assertEqual(hand1.hand, Hand.HIGH_CARD)
        self.assertEqual(hand2.hand, Hand.HIGH_CARD)        
        self.assertEqual(hand1, hand2)
                
        hand2 = get_PokerHand_from_list([10, 19, 26, 34, 50])    
        self.assertEqual(hand1.hand, Hand.HIGH_CARD)
        self.assertEqual(hand2.hand, Hand.HIGH_CARD)
        self.assertGreater(hand1, hand2)
        
    def testPokerHandOnePair(self):        
        hand1 = get_PokerHand_from_list([1, 2, 9, 18, 25, 40])
        self.assertEqual(hand1.hand, Hand.ONE_PAIR)
    
    def testPokerHandTwoPair(self):
        hand1 = get_PokerHand_from_list([1, 2, 9, 10, 18, 25])
        self.assertEqual(hand1.hand, Hand.TWO_PAIR)
    
    def testPokerHandStraight(self):
        hand1 = get_PokerHand_from_list([1, 5, 9, 14, 18])
        self.assertTrue(len(hand1.mean_cards) == 5)
        self.assertEqual(hand1.hand, Hand.STRAIGHT)
        
        hand1 = get_PokerHand_from_list([5, 9, 14, 18, 20])
        self.assertTrue(len(hand1.mean_cards) == 5)
        self.assertEqual(hand1.hand, Hand.STRAIGHT)
        
        hand1 = get_PokerHand_from_list([1, 50, 47, 43, 36])
        self.assertTrue(len(hand1.mean_cards) == 5)
        self.assertEqual(hand1.hand, Hand.STRAIGHT)
        
        hand1 = get_PokerHand_from_list([1, 50, 47, 48, 43, 36])
        self.assertTrue(len(hand1.mean_cards) == 5)
        self.assertEqual(hand1.hand, Hand.STRAIGHT)
    
    def testPokerHandFlush(self):
        hand1 = get_PokerHand_from_list([4, 8, 12, 15, 20, 28])
        self.assertEqual(hand1.hand, Hand.FLUSH)
    
    def testPokerHandFullHouse(self):
        hand1 = get_PokerHand_from_list([4, 5, 6, 19, 18, 30, 38])
        self.assertEqual(hand1.hand, Hand.FULL_HOUSE)

    def testPokerHandFourOfAKind(self):
        hand1 = get_PokerHand_from_list([4, 5, 6, 7, 19, 18, 30])
        self.assertEqual(hand1.hand, Hand.FOUR_OF_A_KIND)

    def testPokerHandStraightFlush(self):
        hand1 = get_PokerHand_from_list([4, 8, 12, 16, 20, 24])
        self.assertEqual(hand1.hand, Hand.STRAIGHT_FLUSH)
    
if __name__ == "__main__":    
    unittest.main()