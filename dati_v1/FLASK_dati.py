#-*-coding:utf-8-*-
from flask import Flask,render_template,session
from flask import request
from flask import redirect
from flask import jsonify
import argparse
import json
import glob
import pickle
import os
import time
import config as C
import datetime
import check_file as check
import random
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config['SECRET_KEY'] = 'zhouchichun'

@app.route("/",methods=["POST","GET"])
@app.route("/index",methods=["POST","GET"])
def index():#首页，分流学生和老师
    return render_template("_index.html",is_login=False)

@app.route("/logout",methods=["POST","GET"])
def logout():#登出模块，清楚cookie
    try:
        session.pop("user")
    except:
        pass
    return render_template("_index.html",is_login=False)


@app.route("/student",methods=["POST","GET"])
def student():
    if request.method=="GET":
        if session.get("user","") in all_name:
            return  render_template("_main_student.html",user=session.get("user"),is_login=True,query=Q.t_question)
        return render_template("_login_student.html",names=all_name,is_login=False)
    else:
        this_name=request.form.get("student_name")
        this_passwd=request.form.get("student_passwd")
        if t_name2passwd[this_name]==this_passwd:
            this_ip= request.remote_addr
            time_now= time.strftime('%Y-%m-%d %H:%M:%S')
            this_x =request.form.get("x")
            this_y=request.form.get("y")
            this_city=request.form.get("city")
            this_pro=request.form.get("pro")
            insert(this_name,this_ip,time_now,this_x,this_y,this_city,this_pro)
            session["user"]=this_name
            return "suc"
        else:
            return "fail"


@app.route("/submit_student",methods=["POST","GET"])
def submit_student():
    if request.method=="GET":
        if session.get("user","") not in all_name:
            return render_template("_index.html")
        return render_template("_main_student.html",user=session.get("user"),is_login=True,query=Q.t_question)
    
    if session.get("user","") in all_name:
        ans_student={}
        for i in range(1,21):
            the_ans=request.form.get(str(i))
            print(the_ans)
            if the_ans in [""] or the_ans==None:
                continue
            an_ls=the_ans.split(",")
            ans_student[str(i)]=an_ls
        state=commit_history(session["user"],ans_student)
        if state=="ok":
       
            return "suc"
        else:
            return "fail"
    else:
        return "fail"

def commit_history(user,ans):
    correct=Q.t_answer
   # print(correct)
   # print(ans)
    record={}
    try:
        for idd,an in correct.items():
            #print(ans[idd])
            if set(an)==set(ans[idd]):
                record[idd]=[True,an,ans[idd]]
            else:
                record[idd]=[False,an,ans[idd]]
        print(record)
        Q.history[user]["anser"]=record
        return "ok"
    except Exception as e:
        print(e)
        return "fail"
@app.route("/get_history",methods=["POST","GET"])
def get_history():
    if session.get("user","")!=C.teacher:
         return "fail"#render_template("_index.html")
    try:
        name_save="static/%s_%s.txt"%(C.teacher,int(random.random()*1000))
        with open(name_save,"w",encoding="utf-8")as f:
            for name, content in Q.history.items():
                time_now=content["time"]
                ip=content["ip"]
                x=content["x"]
                y=content["y"]
                city=content["city"]
                pro=content["pro"]

                f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t"%(name,time_now,ip,x,y,city,pro))
                for idd,con in sorted(content["anser"].items(),key=lambda x:int(x[0])):
                    f.write("%s\t%s\t"%(idd,con[0]))
                f.write("\n")
        return name_save
    except Exception as e:
        print(e)
        return "fail"

                
   



def insert(this_name,this_ip,time_now,this_x,this_y,this_city,this_pro):
    if this_name not in Q.history:
        Q.history[this_name]={}
        Q.done +=1
    Q.history[this_name]["time"]=time_now
    Q.history[this_name]["ip"]=this_ip    
    Q.history[this_name]["x"]=this_x
    Q.history[this_name]["y"]=this_y
    Q.history[this_name]["city"]=this_city
    Q.history[this_name]["pro"]=this_pro
        
@app.route("/main_student",methods=["POST","GET"])
def main_student():
    if session.get("user","") not in all_name: 
        return render_template("_index.html")
    return render_template("_main_student.html",user=session.get("user"),is_login=True,query=Q.t_question)    



@app.route("/teacher",methods=["POST","GET"])
def teacher():
    if request.method=="GET":
        if session.get("user","")==C.teacher:#如果已经登录，直接进入主页面
            return render_template("_main_teacher.html",user=C.teacher,done=Q.done,total=Q.all,is_login=True)
        else:#否则，进入登录页面    
            return render_template("_login_teacher.html",teacher_name=C.teacher,is_login=False)
    else:#验证密码        
        this_passwd=request.form.get("teacher_passwd")
        if this_passwd==C.passwd:
            session["user"]=C.teacher
            return "suc"
        else:
            return "fail"

@app.route("/main_teacher",methods=["POST","GET"])
def main_teacher():
    if session.get("user","")==C.teacher:
        return render_template("_main_teacher.html",user=C.teacher,done=Q.done,total=Q.all,is_login=True)
    else:
        return render_template("_login_teacher.html",teacher_name=C.teacher,is_login=False)


@app.route("/upload",methods=["POST","GET"])
def new_exame():
    #检查是否是老师登录
    if session.get("user","")!=C.teacher:
        return render_template("_login_teacher.html",teacher_name=C.teacher,is_login=False)
    if request.method=="GET":
        return render_template("_upload_file.html",user=C.teacher,is_login=True)
    else:
        #print(request.files)        
        #print("======================")
        f_=request.files["file"]
        now_=time.strftime('%Y_%m_%d_%H_%M_%S')#datetime.datetime.strptime(string,'%Y_%m_%d_%H_%M_%S')
        save_path="static/exame_%s"%(now_)
        f_.save(save_path)
        t_question,t_answer=check.check_file(save_path)
        if t_question=="shibai":
            return "faile" 
        Q.t_question=t_question
        Q.t_answer=t_answer
        Q.done=0
        Q.history={}   
        return "suc"



class today_question():
    def __init__(self,num_student):
        self.t_question={}
        self.t_answer={}
        self.done=0
        self.all=num_student
        self.history={}
    


def init_names():
    t_name2passwd={}
    all_name=[]
    for line in open(C.name2passwd,"r",encoding="utf-8"):
        name,passwd=line.strip().split("\t")
        t_name2passwd[name]=passwd
        all_name.append(name)
    return all_name,t_name2passwd





if __name__=="__main__":
    all_name,t_name2passwd=init_names()
    Q=today_question(len(all_name))
    

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=9100, type=int, help='开启服务的端口号')
    args = parser.parse_args()

    app.run(host="0.0.0.0",port=args.port,debug=True,threaded=True)
    #print test("ST烯碳董事郭社乐辞职曾任公司财务总监遭深交所通报批评")
