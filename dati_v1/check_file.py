def check_file(path):
    question={}
    correct_answer={}
    this_question={"tigan":"","xuanxaing":""}
    idd=-1
    anser=[]
    tigan=""
    for line in open(path,"r",encoding="utf-8"):
        if line.strip() in [""]:
            continue
        if line.find("{}")!=-1:
            if idd!=-1:
                if anser==[] or "A" not in this_question["xuanxiang"]:
                    print(idd)
                    print(this_question)
                    print(anser)
                    return "shibai","shibai"
 
                question[idd]=this_question
                correct_answer[idd]=anser
                this_question={}
                anser=[]
            idd=line.strip().split("{}")[0]
            tigan="{}".join(line.strip().split("{}")[1:])
            this_question["tigan"]=tigan
            this_question["xuanxiang"]={} 
            continue
        if line.find('[A]')!=-1 or line.find('[B]')!=-1 or line.find('[C]')!=-1 or line.find('[D]')!=-1:
            if line.find("[[")!=-1 and line.find("]]")!=-1:
                which,content=line.strip().split("[[")[-1].split("]]")
                anser.append(which)
            else:
                which,content=line.strip().split("[")[-1].split("]")
            this_question["xuanxiang"][which]=content
    question[idd]=this_question
    correct_answer[idd]=anser
    if len(question)>20:
        return "shibai"
    return question,correct_answer

if __name__=="__main__":
    path="static/muban.txt"
    t,a=check_file(path)
    print(t)
    print(a)    
