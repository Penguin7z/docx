# coding=utf-8
from __future__ import division
import pandas as pd
import numpy as np
from common import bi_use_fun
from util import tbl_fun

order_db = tbl_fun.get_order_tbl()
user_c_db = tbl_fun.get_user_c_tbl()
api_call_log_db = tbl_fun.get_api_call_log_tbl()
user_b_db = tbl_fun.get_user_b_tbl()
park_info_db = tbl_fun.get_park_info_tbl()
entry_action_db = tbl_fun.get_entry_action_log_tbl()

order1 = pd.DataFrame(list(order_db.find({'c': {'$gte': 1496246400000, '$lt': 1498838400000}, 'pay_sta': 3},
                                         {'_id': 0, 'paer_id': 1, 'pe_id': 1, 'pay_from': 1, 'or_num': 1,'com_name':1})))
user_c1 = pd.DataFrame(list(user_c_db.find({}, {'r': 1, 'mobile': 1})))
order1 = pd.merge(order1, user_c1, left_on='paer_id', right_on='_id')
len(order1)
len(order1[order1['r'] > 0])
len(order1[~order1['pe_id'].isin(np.array([25905, 34840]))])
len(user_c1[user_c1['r'] > 0])
len(order1[order1['pay_from'] == 2])
len(order1.loc[(order1['r'] > 0) & (~order1['pe_id'].isin(np.array([25905, 34840])))])

coupon_db = tbl_fun.get_activity_s_tbl()
coupon = pd.DataFrame(list(coupon_db.find({}, {'_id': 0, 'id': 1, 't_b': 1, 't_e': 1})))
coupon[u'开始日期'] = bi_use_fun.add_day_info(coupon['t_b'])
coupon[u'结束日期'] = bi_use_fun.add_day_info(coupon['t_e'])

coupon_dis_db = tbl_fun.get_activity_s_bind_c_tbl()
coupon_dis = pd.DataFrame(list(coupon_dis_db.find({}, {'hd_id': 1, 'price': 1, 'is_use': 1, '_id': 0})))

dis_price = coupon_dis.groupby('hd_id').apply(sum).drop('hd_id', axis=1)
dis_cnt = coupon_dis['hd_id'].value_counts()
use_paric = coupon_dis[coupon_dis['is_use'] == 1].groupby('hd_id').apply(sum).drop(['hd_id', 'is_use'], axis=1)
result = pd.concat([dis_cnt, dis_price, use_paric], axis=1)
col = [u'发放张数', u'使用张数', u'发放金额', u'使用金额']
result.columns = col

result = result.reset_index()
result = pd.merge(result, coupon, how='left', left_on='index', right_on='id')

park_info1 = pd.DataFrame(list(park_info_db.find({'name': '长宁德必易园'}, {'park_id': 1})))
app_use_log = pd.DataFrame(list(api_call_log_db.aggregate([{'$match': {'bi_u_o_t': {'$exists': True}}},
                                                           {'$group': {'_id': '$userid'}}])))
user_b1 = pd.DataFrame(list(user_b_db.find({'park_id': park_info1['_id'].values[0]}, {'_id': 1})))
user_c = pd.DataFrame(list(user_c_db.find({'pid': {'$in': list(user_b1['_id'].values)}})))

app_user = bi_use_fun.is_app_user()
app_df = pd.DataFrame(list(user_c_db.find({'_id': {'$in': app_user}}, {'r': 1, 'pid': 1})))
app_df = app_df[app_df['r'] > 0]
park_info2 = pd.DataFrame(list(park_info_db.find({}, {'name': 1})))
user_b2 = pd.DataFrame(list(user_b_db.find({}, {'_id': 1, 'park_id': 1, 'com_name': 1})))
user_b2.columns = ['pid', 'com_name', 'park_id']
park_info2.columns = ['park_id', 'park_name']
app_df = app_df.merge(user_b2, on='pid')
app_df = app_df.merge(park_info2, on='park_id')
result = app_df['park_name'].value_counts()

c_store = pd.DataFrame(
    list(order_db.find({'pe_id': 25905, 'c': {'$gte': 1489852800000, '$lt': 1496073600000}, 'pay_sta': 3},
                       {'or_num': 1, 'c': 1})))
c_store['day'] = bi_use_fun.add_day_info(c_store['c'])
cc = c_store.groupby('day').size()
pd.DataFrame(cc).to_excel('c_store.xlsx')

# 计算非会员登录数
tmp1 = pd.DataFrame(list(api_call_log_db.aggregate([
    {'$match': {'log_c': {'$gte': 1496739600000, '$lt': 1496826000000},
                'fun_name': {'$in': ['hy_login', 'hy_load_userinfo_by_openid']}}},
    {'$group': {'_id': '$userid'}}])))
user1 = pd.DataFrame(list(user_c_db.find({'_id': {'$in': list(tmp1['_id'].values)}}, {'r': 1})))

angel_votes = pd.DataFrame(list(api_call_log_db.find(
    {'fun_name': 'hd_add_angel_votes', 'hd_id': '380122', 'log_c': {'$gte': 1497888000000}, 'status': 200},
    {'_id': 0, 'log_c': 1, 'userid': 1})))
angel_votes = pd.merge(angel_votes, user_c1, left_on='userid', right_on='_id')
len(set(angel_votes['userid'][angel_votes['r'] > 0]))
len(set(angel_votes['userid'][~(angel_votes['r'] > 0)]))

# 最美社群天使投票重复度计算
vote_tb = pd.DataFrame(
    list(api_call_log_db.find({'fun_name': 'hd_add_angel_votes', 'u_id': {'$exists': True}, 'status': 200,
                               'hd_id': '380122'},
                              {'_id': 0, 'u_id': 1, 'userid': 1, 'log_c': 1})))
vote_tb_gp = vote_tb.groupby('u_id')
vote_r = pd.DataFrame()
for id, group in vote_tb_gp:
    total = len(set(group['userid']))
    cnt2 = sum(group['userid'].value_counts() > 1)
    cnt3 = sum(group['userid'].value_counts() > 2)
    cnt4 = sum(group['userid'].value_counts() > 3)
    cnt5 = sum(group['userid'].value_counts() > 4)
    cnt6 = sum(group['userid'].value_counts() > 5)
    temp = pd.DataFrame(
        data=[[id, total, cnt2, cnt2 / total, cnt3, cnt3 / total, cnt4, cnt4 / total, cnt5, cnt5 / total, cnt6,
               cnt6 / total]],
        columns=['_id', u'总投票人数', u'2次以上投票人数', u'2次占比', u'3次以上投票人数', u'3次占比',
                 u'4次以上投票人数', u'4次占比', u'5次以上投票人数', u'5次占比', u'6次以上投票人数', u'6次占比'])
    vote_r = pd.concat([temp, vote_r])
user_angel = pd.DataFrame(list(user_c_db.find({}, {'name': 1})))
vote_r['_id'] = vote_r['_id'].astype(int)
vote_r = pd.merge(vote_r, user_angel, on='_id')
vote_r.to_excel(u'/Users/dingweihua/Documents/dobe/doc/开发/数据分析/最美wehomer投票统计0706.xlsx', index=False)

angel_act = pd.DataFrame(list(entry_action_db.find({'ref_id': 380122}, {'_id': 0})))
main_page_enter = angel_act.loc[(angel_act['page'] == '/static/new_c/dist/views/events/angels/main.html') &
                                (angel_act['event_type'] == 1)]
main_page_enter = main_page_enter.merge(user_c1, left_on='u_id', right_on='_id')
main_page_cnt = len(set(main_page_enter['u_id']))
main_page_member = len(set(main_page_enter['u_id'][main_page_enter['r'] > 0]))
main_page_nomenber = len((set(main_page_enter['u_id'][~(main_page_enter['r'] > 0)])))
s_link = pd.DataFrame(
    list(api_call_log_db.find({'fun_name': 's_link', 'entry_type': '40'}, {'_id': 0, 'log_c': 1, 'userid': 1})))
app_cnt = len(s_link)
vote_df = pd.DataFrame(
    list(api_call_log_db.find({'fun_name': 'hd_add_angel_votes', 'status': 200,
                               'hd_id': '380122'},
                              {'_id': 0, 'u_id': 1, 'userid': 1, 'log_c': 1})))
vote_df = vote_df.merge(user_c1, left_on='userid', right_on='_id')
vote_cnt = len(set(vote_df['userid']))
vote_member = len(set(vote_df['userid'].loc[vote_df['mobile'] > '']))
vote_nomember = len(set(vote_df['userid'].loc[vote_df['mobile'] <= '']))

app_user = bi_use_fun.is_app_user()
hy_vote = vote_df.loc[vote_df['r'] > 0]
app_vote = hy_vote.loc[hy_vote['userid'].isin(np.array(app_user))]
app_vote = app_vote[['userid']]
vote_user_c = pd.DataFrame(list(user_c_db.find({}, {'name': 1, 'pid': 1, 'mobile': 1})))
app_vote = pd.merge(app_vote, vote_user_c, left_on='userid', right_on='_id')
app_vote = pd.merge(app_vote, user_b2, on='pid').drop_duplicates()
app_vote = pd.merge(app_vote, park_info2, on='park_id')
app_vote = app_vote.drop('park_id', axis=1)

# 拉取每个园区公司情况
user_b3 = pd.DataFrame(
    list(user_b_db.find({'state': 1},
                        {'bl_name': 1, 'com_name': 1, 'contacts': 1, 'con_mob': 1, 'pro_type': 1, 'park_id': 1})))
user_c3 = pd.DataFrame(list(user_c_db.find({'r': {'$gt': 0}}, {'pid': 1})))
pid_mem_cnt =user_c3['pid'].value_counts()
pid_mem_cnt.name = u'会员人数'
pid_mem_cnt = pd.DataFrame(pid_mem_cnt)
pid_mem_cnt = pid_mem_cnt.reset_index(col_fill='pid')
pid_mem_cnt.columns = ['pid',u'会员人数']
user_b3 = user_b3.merge(pid_mem_cnt,how='left',left_on='_id',right_on='pid')
user_b3 = user_b3.merge(park_info2,on='park_id')
user_b3 = user_b3.drop(['park_id','pid'],axis=1)
user_b3[u'会员人数'] = user_b3[u'会员人数'].replace(np.nan,0).astype(int)