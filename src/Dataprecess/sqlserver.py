'''
Created on 2013-12-30

@author: Administrator
'''

import pyodbc

if __name__ == '__main__':
    conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=210.30.97.141;DATABASE=sina;UID=zhaoxingli;PWD=admin')
    #outfile1 = open(r'E:\sinadata\userprofile.txt','w')
    #outfile2 = open(r'E:\sinadata\status.txt','w')
    #outfile3 = open(r'E:\sinadata\relation.txt','w')
    outfile4 = open(r'E:\sinadata\comment.txt','w')
    cursor=conn.cursor()
    outfile = outfile4
    con1="SELECT [user_id],[screen_name],[name],[province]\
          ,[city]\
          ,[location]\
          ,[description]\
          ,[gender]\
          ,[followers_count]\
          ,[friends_count]\
          ,[statuses_count]\
          ,[favourites_count]\
          ,[created_at]\
      FROM [sina].[dbo].[users]"
    con2="SELECT [user_id],[status_id]\
      ,[created_at]\
      ,[content]\
      ,[source_name]\
      ,[favorited]\
      ,[retweeted_status_id]\
  FROM [sina].[dbo].[statuses]"
    con3="SELECT [source_user_id]\
      ,[target_user_id]\
      ,[relation_state]\
      ,[update_time]\
  FROM [sina].[dbo].[user_relation]"
    con4="SELECT [comment_id]\
      ,[content]\
      ,[created_at]\
      ,[user_id]\
      ,[status_id]\
      ,[update_time]\
  FROM [sina].[dbo].[comments] "
    cursor.execute(con4)
    #for c in cursor.next():
    try:
        line = 0
        while 1:
            temp=cursor.fetchone()
            if not temp:
                break
            line += 1
            for c in temp:
                c = ' '.join(str(c).split())
                outfile4.write(str(c).strip()+'\t')
            outfile4.write('\n')
            if line%10000==0:
                print line
       # temp = cursor.fetchone()
    finally:
        print line
        cursor.close()
        outfile4.close()

