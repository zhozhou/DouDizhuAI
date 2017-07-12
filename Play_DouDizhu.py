import random

#配置出牌规则
ALLOW_THREE_ONE = True
ALLOW_THREE_TWO = False
ALLOW_FOUR_TWO = True

#定义牌型
class COMB_TYPE:
	PASS, SINGLE, PAIR, TRIPLE, TRIPLE_ONE, TRIPLE_TWO, FOURTH_TWO_ONES, FOURTH_TWO_PAIRS, STRIGHT, BOMB, KING_PAIR = range(11)

	
#斗地主程序，启动后模拟3个玩家洗牌，抓拍，套路出牌，到最终分出胜负。
class Doudizhu:
    def __init__(self):
	    #定义牌的映射值
        self.a=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,
                19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,
                36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53]
        #本局玩家持有牌数组[[],[],[]]
		self.users=[]
		#历史出牌的内容
        self.handout_hist=[]

	#洗牌，随机生成54个数的数组，并抽掉一个数
    def xipai(self):
        random.shuffle(self.a)
        n=random.randint(1,54)
        b=self.a[:n]
        c=self.a[n:]
        self.a=c+b
		
    #发牌，最后留3张，其他分3份
    def fapai(self):
        self.str1=self.a[:-3:3]
        self.str2=self.a[1:-3:3]
        self.str3=self.a[2:-3:3]
        self.str4=self.a[-3:]

	#随机指定一个地主
    def qiangdizhu(self):
        n=random.randint(0,2)
        self.dizhu=n
        print "dizhu is user"+str(n)
        if n==0:
            self.str1+=self.str4
        if n==1:
            self.str2+=self.str4
        if n==2:
            self.str3+=self.str4

	#对牌进行升序排序，方便计算出牌的排列组合
    def mapai(self):
        self.str1.sort()
        self.str2.sort()
        self.str3.sort()

	#牌面和洗牌id的映射
    def yingshe(self):
        paizd=[(0,'3'),(1,'3'),(2,'3'),(3,'3'),
               (4,'4'),(5,'4'),(6,'4'),(7,'4'),
               (8,'5'),(9,'5'),(10,'5'),(11,'5'),
               (12,'6'),(13,'6'),(14,'6'),(15,'6'),
               (16,'7'),(17,'7'),(18,'7'),(19,'7'),
               (20,'8'),(21,'8'),(22,'8'),(23,'8'),
               (24,'9'),(25,'9'),(26,'9'),(27,'9'),
               (28,'10'),(29,'10'),(30,'10'),(31,'10'),
               (32,'11'),(33,'11'),(34,'11'),(35,'11'),
               (36,'12'),(37,'12'),(38,'12'),(39,'12'),
               (40,'13'),(41,'13'),(42,'13'),(43,'13'),
               (44,'14'),(45,'14'),(46,'14'),(47,'14'),
               (48,'15'),(49,'15'),(50,'15'),(51,'15'),
               (52,'16'),(53,'17')]

        zdpai = dict(paizd)
        paistr1=''
        for i in range (len(self.str1)):
            paistr1+=zdpai[self.str1[i]]+' '
        paistr2=''
        for i in range (len(self.str2)):
            paistr2+=zdpai[self.str2[i]]+' '
        paistr3=''
        for i in range (len(self.str3)):
            paistr3+=zdpai[self.str3[i]]+' '
        self.users.append([int(x) for x in paistr1.strip().split(' ')])
        self.users.append([int(x) for x in paistr2.strip().split(' ')])
        self.users.append([int(x) for x in paistr3.strip().split(' ')])
        print self.users
	
	
    #出牌大小比较:comb2是否比comb1大
    def can_comb2_beat_comb1(comb1, comb2):
        if comb2['type'] == COMB_TYPE.PASS:
            return False
    
        if not comb1 or comb1['type'] == COMB_TYPE.PASS:
            return True
    
        if comb1['type'] == comb2['type']:
            if comb1['type'] == COMB_TYPE.STRIGHT:
                if comb1['main'] != comb2['main']:
                    return False
                else:
                    return comb2['sub'] > comb1['sub']
            else:
                if comb1['main'] == comb2['main'] and comb1['type']<>COMB_TYPE.PAIR and comb1['type']<>COMB_TYPE.TRIPLE and comb1['type']<>COMB_TYPE.SINGLE:
                    return comb2['sub'] > comb1['sub']
                else:
                    return comb2['main'] > comb1['main']
        elif comb2['type'] == COMB_TYPE.BOMB or comb2['type'] == COMB_TYPE.KING_PAIR:
            return comb2['type'] > comb1['type']
    
        return False
    
    
    #从持有牌中计算所有可以出牌类型的排列组合
    def get_all_hands(self,pokers):
        if not pokers:
            return []
    
        combs = [{'type':COMB_TYPE.PASS,'name':'PASS'}]
        dic = {}
        for poker in pokers:
            dic[poker] = dic.get(poker, 0) + 1
    
        for poker in dic:
            if dic[poker] >= 1:
                #SINGLE
                combs.append({'type':COMB_TYPE.SINGLE,'name':'SINGLE', 'main':poker})
            if dic[poker] >= 2:
                #PAIR
                combs.append({'type':COMB_TYPE.PAIR,'name':'PAIR', 'main':poker})
            if dic[poker] >= 3:
                #TRIPLE
                combs.append({'type':COMB_TYPE.TRIPLE,'name':'TRIPLE', 'main':poker})
                for poker2 in dic:
                    if ALLOW_THREE_ONE and dic[poker2] >= 1 and poker2 != poker:
                        #TRIPLE_ONE
                        combs.append({'type':COMB_TYPE.TRIPLE_ONE,'name':'TRIPLE_ONE', 'main':poker, 'sub':poker2})
                    if ALLOW_THREE_TWO and dic[poker2] >= 2 and poker2 != poker:
                        #TRIPLE_TWO
                        combs.append({'type':COMB_TYPE.TRIPLE_TWO,'name':'TRIPLE_TWO', 'main':poker, 'sub':poker2})
                            
            if dic[poker] == 4:
                #BOMB
                combs.append({'type':COMB_TYPE.BOMB, 'name':'BOMB','main':poker})
                if ALLOW_FOUR_TWO:
                    pairs = []
                    ones = []
                    for poker2 in dic:
                        if dic[poker2] == 1:
                            ones.append(poker2)
                        elif dic[poker2] == 2:
                            pairs.append(poker2)
                    for i in xrange(len(ones)):
                        for j in xrange(i + 1, len(ones)):
                            combs.append({'type':COMB_TYPE.FOURTH_TWO_ONES,'name':'FORTH_TWO_ONES', 'main':poker, 'sub1':ones[i], 'sub2':ones[j]})
                    for i in xrange(len(pairs)):
                        combs.append({'type':COMB_TYPE.FOURTH_TWO_ONES,'name':'FORTH_TOW_ONES', 'main':poker, 'sub1':pairs[i], 'sub2':pairs[i]})
                        for j in xrange(i + 1, len(pairs)):
                            combs.append({'type':COMB_TYPE.FOURTH_TWO_PAIRS,'name':'FOURTH_TWO_PAIRS', 'main':poker, 'sub1':pairs[i], 'sub2':pairs[j]})
    
        if 16 in pokers and 17 in pokers:
            #KING_PAIR
            combs.append({'type':COMB_TYPE.KING_PAIR,'name':'KING_PAIR'})
    
        #STRIGHT
        distincted_sorted_pokers = sorted(list(set(pokers)))
        lastPoker = distincted_sorted_pokers[0]
        sequence_num = 1
        i = 1
        while i < len(distincted_sorted_pokers):
            # Only 3-A Can be STRIGHT
            if distincted_sorted_pokers[i] <= 14 and distincted_sorted_pokers[i] - lastPoker == 1:
                sequence_num += 1
                if sequence_num >= 5:
                    j = 0
                    while sequence_num - j >= 5:
                        #STRIGHT
                        combs.append({'type':COMB_TYPE.STRIGHT,'name':'STRIGHT', 'main':sequence_num - j, 'sub':distincted_sorted_pokers[i]})
                        j += 1
            else:
                sequence_num = 1
            lastPoker = distincted_sorted_pokers[i]
            i += 1
    
        return combs

	#出牌后把出掉的牌从持有牌中剔除，返回剩余的牌
    def make_hand(pokers, hand):
        poker_clone = pokers[:]
        if hand['type'] == COMB_TYPE.SINGLE:
            poker_clone.remove(hand['main'])
        elif hand['type'] == COMB_TYPE.PAIR:
            poker_clone.remove(hand['main'])
            poker_clone.remove(hand['main'])
        elif hand['type'] == COMB_TYPE.TRIPLE:
            poker_clone.remove(hand['main'])
            poker_clone.remove(hand['main'])
            poker_clone.remove(hand['main'])
        elif hand['type'] == COMB_TYPE.TRIPLE_ONE:
            poker_clone.remove(hand['main'])
            poker_clone.remove(hand['main'])
            poker_clone.remove(hand['main'])
            poker_clone.remove(hand['sub'])
        elif hand['type'] == COMB_TYPE.TRIPLE_TWO:
            poker_clone.remove(hand['main'])
            poker_clone.remove(hand['main'])
            poker_clone.remove(hand['main'])
            poker_clone.remove(hand['sub'])
            poker_clone.remove(hand['sub'])
        elif hand['type'] == COMB_TYPE.FOURTH_TWO_ONES:
            poker_clone.remove(hand['main'])
            poker_clone.remove(hand['main'])
            poker_clone.remove(hand['main'])
            poker_clone.remove(hand['main'])
            poker_clone.remove(hand['sub1'])
            poker_clone.remove(hand['sub2'])
        elif hand['type'] == COMB_TYPE.FOURTH_TWO_PAIRS:
            poker_clone.remove(hand['main'])
            poker_clone.remove(hand['main'])
            poker_clone.remove(hand['main'])
            poker_clone.remove(hand['main'])
            poker_clone.remove(hand['sub1'])
            poker_clone.remove(hand['sub1'])
            poker_clone.remove(hand['sub2'])
            poker_clone.remove(hand['sub2'])
        elif hand['type'] == COMB_TYPE.STRIGHT:
            for i in xrange(hand['sub'], hand['sub'] - hand['main'], -1):
                poker_clone.remove(i)
        elif hand['type'] == COMB_TYPE.BOMB:
            poker_clone.remove(hand['main'])
            poker_clone.remove(hand['main'])
            poker_clone.remove(hand['main'])
            poker_clone.remove(hand['main'])
        elif hand['type'] == COMB_TYPE.KING_PAIR:
            poker_clone.remove(16)
            poker_clone.remove(17)
        return poker_clone
		
	#上游PASS之后，我方主动出牌策略：
	#循环持有牌的所有出牌可能，优先顺序为3带x，顺子，对子，单牌，炸弹，王炸
	#同种牌里面，找到最小的出
    def handout_maxnum(self,all_hands):
        the_triple_two=None
        the_triple_one=None
        the_triple=None
        the_pair=None
        the_single=None
        the_bomb=None
        the_kingpair=None
        the_stright=None    

        for hand in all_hands:

            if hand['type']==COMB_TYPE.TRIPLE_TWO:
                if the_triple_two is None:
                    the_triple_two=hand
                elif self.can_comb2_beat_comb1(hand,the_triple_two):
                    the_triple_two=hand
            elif hand['type']==COMB_TYPE.TRIPLE_ONE:
                if the_triple_one is None:
                    the_triple_one=hand
                elif self.can_comb2_beat_comb1(hand,the_triple_one):
                    the_triple_one=hand
            elif hand['type']==COMB_TYPE.TRIPLE:
                if the_triple is None:
                    the_triple=hand
                elif self.can_comb2_beat_comb1(hand,the_triple):
                    the_triple=hand
			            if hand['type']==COMB_TYPE.STRIGHT:
            elif the_stright is None:
                    the_stright=hand
                elif self.can_comb2_beat_comb1(hand,the_stright):
                    the_stright=hand
            elif hand['type']==COMB_TYPE.PAIR:
                if the_pair is None:
                    the_pair=hand
                elif self.can_comb2_beat_comb1(hand,the_pair):
                    the_pair=hand
            elif hand['type']==COMB_TYPE.SINGLE:
                if the_single is None:
                    the_single=hand
                elif self.can_comb2_beat_comb1(hand,the_single):
                    the_single=hand
            elif hand['type']==COMB_TYPE.BOMB:
                if the_bomb is None:
                    the_bomb=hand
                elif self.can_comb2_beat_comb1(hand,the_bomb):
                    the_bomb=hand
            elif hand['type']==COMB_TYPE.KING_PAIR:
                if the_kingpair is None:
                    the_kingpair=hand
                elif self.can_comb2_beat_comb1(hand,the_kingpair):
                    the_kingpair=hand
              
        if the_stright is not None:
            return the_stright
        elif the_triple_two is not None:
            return the_triple_two
        elif the_triple_one is not None:
            return the_triple_one
        elif the_triple is not None:
            return the_triple
        elif the_pair is not None:
            return the_pair
        elif the_single is not None:
            return the_single
        elif the_bomb is not None:
            return the_bomb
        elif the_kingpair is not None:
            return the_kingpair
        else:
            print 'Unknown type'
            return all_hands[0]
        

    #依据上游历史出牌的内容，决定本次出牌的内容
    def hand_out(self,last_handout,handout_seq):
        cur_player=(self.dizhu + handout_seq) % 3
        all_hands=self.get_all_hands(self.users[cur_player])

        if handout_seq>=2:
            before_lasthandout=self.handout_hist[handout_seq-2]

        handout={'type':COMB_TYPE.PASS,'name':'PASS'}
		#第一次出牌，或者上游PASS以及上上游PASS, 本次为主动出牌策略
        if handout_seq==0 or (handout_seq>0 and last_handout['type'] == COMB_TYPE.PASS and before_lasthandout['type'] == COMB_TYPE.PASS):
            #主动出牌策略
			handout=self.handout_maxnum(all_hands)
                
        else:
		    #被动出牌策略:找到能大住上次出牌的牌，或者大住上上次出牌的牌
			#由于排序是按照升序排序，出牌会自动选择能大住，但最小的牌打出
            for hand in all_hands:
                if last_handout['type']<>COMB_TYPE.PASS and self.can_comb2_beat_comb1(last_handout,hand):
                    handout=hand
                elif last_handout['type']==COMB_TYPE.PASS and before_lasthandout<>COMB_TYPE.PASS and self.can_comb2_beat_comb1(before_lasthandout,hand):
                    handout=hand 
        
		#打印出牌日志
        print "\r\nseq_no:",handout_seq
        if cur_player==self.dizhu:
            print "dizhu:user"+str(cur_player)+":"+str(self.users[cur_player])
            print "dizhu:user"+str(cur_player)+":"+str(handout)
        else:
            print "farmer:user"+str(cur_player)+":"+str(self.users[cur_player])
            print "farmer:user"+str(cur_player)+":"+str(handout)

		#出牌后剔除已出的牌
        self.users[cur_player]=self.make_hand(self.users[cur_player],handout)

		#如果剔除完成后，当前玩家手中无牌，则宣布胜利
        if (len(self.users[cur_player]) == 0):
            self.is_end ='Y'
            print "user"+str(cur_player)+" win"

        return handout


	#开始打牌
    def start(self):
	    self.xipai()
        self.fapai()
        self.qiangdizhu()
        self.mapai()
        self.yingshe()
	
        self.is_end='N'
        handout_seq=0
        while self.is_end <> 'Y':
            if handout_seq==0:
                last_handout={'type':COMB_TYPE.PASS,'name':'PASS'}
            else:
                last_handout=self.handout_hist[handout_seq-1]
 
            current_handout=self.hand_out(last_handout,handout_seq)
            self.handout_hist.append(current_handout)
            handout_seq+=1
            

game=Doudizhu()
game.start()
