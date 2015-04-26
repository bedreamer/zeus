# -*- coding:utf-8 -*-
import sqlite3
import random

class db:
    handle = 0

    def __init__(self, dbname):
        try:
            self.handle = sqlite3.connect(dbname)
        except:
            print('打开数据库失败!')

    def close(self):
        if (self.handle):
            self.handle.close()

    '''新增一个节点'''
    def node_new(self, nid, pid=-1):
        if (self.handle):
            try:
                sql = "INSERT INTO nd VALUES('" + str(nid) + "','" + str(pid) + "')"
                print(sql)
                self.handle.execute(sql)
                self.handle.commit()
            except Exception,ex:
                print Exception,":",ex
                print('新建节点%d.%d失败' % (pid, nid))

    '''新增一个属性记录'''
    def attrib_new(self, nid=-1, key='undefined', value='undefined', seed=0.8):
        if (self.handle):
            try:
                sql = "INSERT INTO attrib VALUES('" + str(nid) + "','" + key + "','" + value + "','" + str(seed) + "')"
                print(sql)
                cur = self.handle.cursor()
                cur.execute(sql)
                self.handle.commit()
            except:
                print("新建属性%d.%s(%s)=%s 失败" % (nid, key, str(value), seed))

    '''复制一个节点, 按照给定概率继承父节点属性'''
    def node_fork(self, nid, seed=0.8, pid=-1):
        if (self.handle):
            try:
                sql = "SELECT key,value,inhrabe FROM attrib WHERE id='" + str(pid) + "'"
                print(sql)
                cur = self.handle.cursor()
                ret = cur.execute(sql)
                attrib_ret = ret.fetchone()
                while ( attrib_ret ):
                    if (attrib_ret[2]==1.0):
                        self.attrib_new(nid, attrib_ret[0], attrib_ret[1], attrib_ret[2])
                    elif ( attrib_ret[2] != 0.0 and random.uniform(0.0, 1.0) <= 0.8 ):
                        self.attrib_new(nid, attrib_ret[0], attrib_ret[1], seed)
                    else:
                        print("discard attribute: " + attrib_ret[0])
                    attrib_ret = ret.fetchone()
                self.node_new(nid, pid)
            except:
                print("继承节点失败.")

    '''打印节点'''
    def node_print(self):
        if (self.handle):
            try:
                sql = "SELECT id FROM nd"
                cur = self.handle.cursor()
                id_ret = cur.execute(sql)
                mid = id_ret.fetchone()
                while (mid):
                    sql = "SELECT key,value FROM attrib WHERE id='" + str(mid[0]) + "'"
                    print(sql)
                    cur = self.handle.cursor()
                    attrib_ret = cur.execute(sql)
                    attrib = attrib_ret.fetchone()
                    while ( attrib ):
                        print( str(mid[0]) + "." +  attrib[0] + " = " + attrib[1])
                        attrib = attrib_ret.fetchone()
                    mid = id_ret.fetchone()
            except:
                print("继承节点失败.")

d = db("/home/tom/workspace/zeus/zeus.db")
d.node_new(6, 1)
d.node_fork(2, 0.8, 1)
d.node_fork(3, 0.8, 1)
d.node_fork(4, 0.8, 1)
d.node_fork(5, 0.8, 1)
d.node_print()
d.close()
