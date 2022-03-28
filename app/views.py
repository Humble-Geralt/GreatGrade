"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from . import models
import numpy as np
from . import predict_model as pm
import time
import random

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'主页',
            'year':datetime.now().year,
        }
    )
#总览页面
def overview(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    teacher_class=[]
    try:
        teacher_class.append(request.user.TeacherClass)
    except:
        teacher_class.append(4)
    #获取所有班级的所有次考试，得到最近考试次数
    class_all_full_prime=models.AllTest.objects.filter(Class=teacher_class[0]).values()
    class_testid=[int(i.get('TesT_id')) for i in list(class_all_full_prime)]
    now_testid=max(class_testid)

    #获得当前班级的所有次数考试，将其打包为各学科值
    class_all_full=models.AllTest.objects.filter(Class=teacher_class[0]).values().order_by('TesT_id')
    class_all=list(class_all_full)
    #初始化列表
    test_id,math,english,chinese,phy,bio,che=[],[],[],[],[],[],[]
    for i in class_all:
        test_id.append('第'+str(i.get('TesT_id'))+'次考试')
        math.append(i.get('Math2'))
        english.append(i.get('English2'))
        chinese.append(i.get('Chinese2'))
        phy.append(i.get('Physics2'))
        bio.append(i.get('Biology2'))
        che.append(i.get('Chemistry2'))

    #print(test_id,math,english,chinese,phy,bio,che)
    
    #获得第选定班级，最近一次考试的所有成绩
    grade_all=models.ClassGrade.objects.filter(TEST_id=now_testid,CLASS=teacher_class[0]).values()
    grade=list(grade_all.order_by('-Total'))

    #获取趋势并计算
    class_total=[int(i.get('total')) for i in list(class_all)]
    if len(class_total)>=2:
        class_trend=int(((class_total[-1]-class_total[-2])/class_total[-2])*100)
    else:
        class_trend=0
    if class_trend>=0:
        class_trends='+'+str(class_trend)
    else:
        class_trends='-'+str(class_trend)
    #以趋势判断学生状态
    if class_trend>=-3 and class_trend <=10:
        stauts='好'
    else:
        if class_trend>=10:
            stauts='非常好'
        else:
            stauts='差'

    #获取顺位并处理
    class_rank= class_all_full_prime.filter(TesT_id=now_testid).order_by('total')
    temp=0
    for i in class_rank:
        temp+=1
        if i.get('Class')==teacher_class[0]:
            rank=temp
        else:
            rank='error'
            temp=0
    #获取班级人数
    class_people=models.ClassGrade.objects.filter(TEST_id=now_testid,CLASS=teacher_class[0]).count()
    #高考天数与月考天数
    next_test=31-datetime.now().day
    next_test_pre=((datetime.now().day)/31)*100
    final_test=(6%datetime.now().month)*30+(7-datetime.now().day)
    final_test_pre=((158-final_test)/158)*100
    return render(
        request,
        'app/GGindex.html',
        {
            'title':'总览/Overview',
            'year':datetime.now().year,
            'next_test':next_test,
            'next_test_precent':int(next_test_pre),
            'final_test':final_test,
            'final_test_precent':int(final_test_pre),
            'now_testid':now_testid,
            'next_testid':now_testid+1,
            'people':class_people,
            'trend':class_trends,
            'grade':grade[:10],
            'testid':test_id,
            'math':math,
            'chinese':chinese,
            'english':english,
            'phy':phy,
            'bio':bio,
            'che':che,
            'rank':rank,
            'stauts': stauts,
        }
    )

def datas_change(request):
    """Renders the datas page."""
    assert isinstance(request, HttpRequest)
    teacher_class=[]
    try:
        teacher_class.append(request.user.TeacherClass)
    except:
        teacher_class.append(4)
    class_inside_prime=models.ClassGrade.objects.filter(CLASS=teacher_class[0]).values()
    class_inside=list(class_inside_prime)
    class_num=class_inside[0].get('CLASS')
    return render(
        request,
        'app/datas_change.html',
        {
            'title':'数据修改/Datas',
            'message':'database contrl page.',
            'year':datetime.now().year,
            'class_info':class_inside,
            'class':class_num,
        }
    )

def datas_search(request):
    """Renders the datas page."""
    assert isinstance(request, HttpRequest)
    #使用GET方法从前端获取搜索学号
    q = request.GET.get('q')
    #判别语句
    search_res=models.ClassGrade.objects.filter(studentNum=q).order_by('TEST_id')
    #如果存在
    if search_res:
        search_grade=list(search_res.values())
        search_name=search_grade[0].get('STName')
        search_class=search_grade[0].get('CLASS')
        test_id,math,english,chinese,phy,bio,che,total=[],[],[],[],[],[],[],[]
        for i in search_grade:
            test_id.append('第'+str(i.get('TEST_id'))+'次考试')
            math.append(i.get('Math3'))
            english.append(i.get('English3'))
            chinese.append(i.get('Chinese3'))
            phy.append(i.get('Physics3'))
            bio.append(i.get('Biology3'))
            che.append(i.get('Chemistry3'))
            total.append(i.get('Total'))
        return render(
            request,
            'app/datas_search.html',
            {
                'title':'数据查询/Datas',
                'message':'Database contrl page.',
                'year':datetime.now().year,
                'res':1,
                'typecode':'has-success',
                'searchmessage':'学号 '+q+' 搜索完成！',
                'search_res':search_res,
                'testid':test_id,
                'math':math,
                'chinese':chinese,
                'english':english,
                'phy':phy,
                'bio':bio,
                'che':che,
                'total':total,
                'name':search_name,
                'class':search_class,
            }
        )
    return render(
            request,
            'app/datas_search.html',
            {
                'title':'数据查询/Datas',
                'message':'Database contrl page.',
                'year':datetime.now().year,
                'res':0,
                'typecode':'',
                'searchmessage':'',
                'search_res':'',
                'testid':'',
                'math':'',
                'chinese':'',
                'english':'',
                'phy':'',
                'bio':'',
                'che':'',
                'total':'',
                'name':'',
                'class':'',
            }
        )

def datas_add(request):
    """Renders the predict page."""
    assert isinstance(request, HttpRequest)
    request.encoding='utf-8'
    res=''
    if request.method =="POST":
        studentid = request.POST.get('studentid')
        testid = request.POST.get('testid')
        sub1 = request.POST.get('sub1')
        sub2 = request.POST.get('sub2')
        sub3 = request.POST.get('sub3')
        sub4 = request.POST.get('sub4')
        sub5 = request.POST.get('sub5')
        sub6 = request.POST.get('sub6')
        #数据库代码1
        if studentid and testid and sub1 and sub2 and sub3 and sub4 and sub5 and sub6:
            total=int(sub1)+int(sub2)+int(sub3)+int(sub4)+int(sub5)+int(sub6)
            if request.POST.get('name') and request.POST.get('classid'):
                if models.ClassGrade.objects.filter(studentNum=studentid,TEST_id=testid):
                    res='已有记录，无法添加此次考试'
                else:
                    name = request.POST.get('name')
                    classid = request.POST.get('classid')
                    models.ClassGrade.objects.create(CLASS=classid,STName=name,studentNum=studentid,TEST_id=testid,Chinese3=sub1,Math3=sub2,English3=sub3,Physics3=sub4,Chemistry3=sub5,Biology3=sub6,Total=total)
                    if models.ClassGrade.objects.filter(studentNum=studentid,TEST_id=testid):
                        res='学号'+str(studentid)+'第'+str(testid)+'次考试,'+'学生'+name+'已成功入库！'
                    else:
                        res='学生'+name+'入库失败！'

            #数据库代码2
            else:
                total=int(sub1)+int(sub2)+int(sub3)+int(sub4)+int(sub5)+int(sub6)
                if models.ClassGrade.objects.filter(studentNum=studentid,TEST_id=testid):
                    res='已有记录，无法添加此次考试'
                else:
                    if models.ClassGrade.objects.filter(studentNum=studentid):
                        student = models.ClassGrade.objects.filter(studentNum=studentid).values()
                        name=list(student)[0].get('STName')
                        classid = list(student)[0].get('CLASS')
                        models.ClassGrade.objects.create(CLASS=classid,STName=name,studentNum=studentid,TEST_id=testid,Chinese3=sub1,Math3=sub2,English3=sub3,Physics3=sub4,Chemistry3=sub5,Biology3=sub6,Total=total)
                        if models.ClassGrade.objects.filter(studentNum=studentid,TEST_id=testid):
                            res='学号'+str(studentid)+'第'+str(testid)+'次考试,'+'学生'+name+'已成功入库！'
                        else:
                            res='学生'+name+'入库失败！'
                    else:
                        res='并非已存在学生'
        else:
            res='参数传入失败，请检查传参格式'
    return render(
        request,
        'app/datas_add.html',
        {
            'title':'数据提交/Datas',
            'message':'Database contrl page.',
            'year':datetime.now().year,
            'res':res
        }
    )

def datas_del(request):
    """Renders the predict page."""
    assert isinstance(request, HttpRequest)
    request.encoding='utf-8'
    res=''
    if request.method =="POST":
        studentid = request.POST.get('studentid')
        testid = request.POST.get('testid')
        testnum = request.POST.get('testnum')
        #数据库代码1
        if studentid and testid:
            student=models.ClassGrade.objects.filter(studentNum=studentid,TEST_id=testid).values()
            if student:
                name=list(student)[0].get('STName')
                models.ClassGrade.objects.filter(studentNum=studentid,TEST_id=testid).delete()
                if not models.ClassGrade.objects.filter(studentNum=studentid,TEST_id=testid):
                    res='学生'+str(name)+'已成功删除第'+str(testid)+'条考试数据！'
                else:
                    res='学生'+str(name)+'删除失败'
            else:
                    res='学生删除失败,无对应记录！'
                #数据库代码2
        else:
            if testnum:
                student=models.ClassGrade.objects.filter(id=testnum).values()
                if student:
                    name=list(student)[0].get('STName')
                    models.ClassGrade.objects.filter(id=testnum).delete()
                    if not models.ClassGrade.objects.filter(studentNum=studentid,TEST_id=testid):
                        res='学生'+str(name)+'已成功删除第'+str(testnum)+'条考试数据！'
                    else:
                        res='学生'+str(name)+'删除失败'
                else:
                    res='学生删除失败,无对应记录！'
            else:
                res='参数传入失败，请检查传参格式'
            
    return render(
        request,
        'app/datas_del.html',
        {
            'title':'数据删除/Datas',
            'message':'Database contrl page.',
            'year':datetime.now().year,
            'res':res
        }
    )

def class_predict(request):
    """Renders the predict page."""
    assert isinstance(request, HttpRequest)
    res,message='',''
    teacher_class=[]
    try:
        teacher_class.append(request.user.TeacherClass)
    except:
        teacher_class.append(4)
    final_score=0
    cost=0
    optimal=[0,0,0]
    res=0
    class_id=''
    test_id=''
    allgrade=''
    avgclass=''
    grade_fir=''
    grade_sec=''
    grade_thr=''
    grade_four=''
    grade_fiv=''
    message_tx=''
    grademin=0
    grademax=0
    if request.method =="POST":
        class_id=request.POST.get('class')
        hard=request.POST.get('hardrank')
        temp=[]
        if class_id and hard:

            #预测部份
            if models.ClassGrade.objects.filter(CLASS=class_id):
                grade_frame=models.ClassGrade.objects.filter(CLASS=class_id).values()
                grade=list(grade_frame)
                grade_final=[]
                max_test=max([i.get('TEST_id') for i in grade])
                for i in grade:
                    if int(i.get('TEST_id'))>=(int(max_test)-4):
                        grade_final.append(i)
                test_id=max(i.get('TEST_id') for i in grade)
                allgrade=list(models.AllClassGrade.objects.filter(test=test_id).values())
                avgclass=list(models.AllTest.objects.filter(TesT_id=test_id,Class=class_id).values())
                grade_fir=models.ClassGrade.objects.filter(CLASS=class_id,TEST_id=test_id,Total__gte=0,Total__lt=400).count()
                grade_sec=models.ClassGrade.objects.filter(CLASS=class_id,TEST_id=test_id,Total__gte=400,Total__lt=500).count()
                grade_thr=models.ClassGrade.objects.filter(CLASS=class_id,TEST_id=test_id,Total__gte=500,Total__lt=550).count()
                grade_four=models.ClassGrade.objects.filter(CLASS=class_id,TEST_id=test_id,Total__gte=550,Total__lt=600).count()
                grade_fiv=models.ClassGrade.objects.filter(CLASS=class_id,TEST_id=test_id,Total__gte=600,Total__lt=750).count()

                x,y=Pretreatment(grade_final,'Total',750)
                pre_model=pm.predict_model()
                pre_model.set_train(x,y)
                final_score,optimal=pre_model.get_res([5,float(hard)])
                final_score=final_score*7.5
                cost=pre_model.cost_function()
                grademin=int(final_score-cost/10)
                if int(final_score+cost/10)<=750:
                    grademax=int(final_score+cost/10)
                else:
                    grademax=750
                    
                message_tx='预测完成'
                res=1
                if models.ClassGrade.objects.filter(CLASS=class_id).count()<=30:
                    message='本次预测数据小于30个，模型可信度<1%'
                else :
                    if 80>models.ClassGrade.objects.filter(CLASS=class_id).count()>30:
                        message='本次预测数据介于30-80个，模型可信度接近15%'
                    else:
                        if 200>models.ClassGrade.objects.filter(CLASS=class_id).count()>80:
                            message='本次预测数据介于80-200个，模型可信度接近60%'
                        else:
                            message='本次预测数据大于200个，模型可信度到达70%以上'
                #普通数据
            else:
                message_tx='无此班数据'
            
        else:
            message_tx='传参错误'
        
    return render(
        request,
        'app/class_predict.html',
        {
            'title':'班级预测/Predict',
            'message':'Predict page.',
            'year':datetime.now().year,
            'message':message_tx,
            'class':teacher_class,
            'premessage':message,
            'res':res,
            'score':int(final_score),
            'theta1':float(optimal[0]),
            'theta2':float(optimal[1]),
            'theta3':float(optimal[2]),
            'grademin':grademin,
            'grademax':grademax,
            'classid':class_id,
            'testid':test_id,
            'avgclass':avgclass,
            'avgall':allgrade,
            'grade_fir':grade_fir,
            'grade_sec':grade_sec,
            'grade_thr':grade_thr,
            'grade_four':grade_four,
            'grade_fiv':grade_fiv,
        }
    )

def subject_predict(request):
    """Renders the predict page."""
    assert isinstance(request, HttpRequest)
    res,message='',''
    teacher_class=[]
    try:
        teacher_class.append(request.user.TeacherClass)
    except:
        teacher_class.append(4)
    final_score=0
    cost=0
    optimal=[0,0,0]
    res=0
    sub_name=''
    test_id=''
    allgrade=''
    avgclass=''
    grade_fir=''
    grade_sec=''
    grade_thr=''
    grade_four=''
    grade_fiv=''
    message_tx=''
    max_score=0
    grademin=0
    grademax=0
    pass_1,unpass_1,pass_2,unpass_2,pass_3,unpass_3=0,0,0,0,0,0
    grade_5,grade_4,grade_3,grade_2,grade_1,grade_0,grade_t=0,0,0,0,0,0,0
    if request.method =="POST":
        sub_name=request.POST.get('sub')
        hard=request.POST.get('hardrank')
        temp=[]
        if sub_name and hard:
            max_score,sub_key=subjects(sub_name)
            if max_score==0:
                message_tx='参数接受错误，请检查格式是否正确'
            else:
                if models.ClassGrade.objects.values(sub_key):
                    grade_frame=models.ClassGrade.objects.values()
                    grade=list(grade_frame)
                    test_id=max(i.get('TEST_id') for i in grade)
                    grade_final=[]
                    max_test=max([i.get('TEST_id') for i in grade])
                    for i in grade:
                        if int(i.get('TEST_id'))>=(int(max_test)-4):
                            grade_final.append(i)
                    test_id=max(i.get('TEST_id') for i in grade)

                    allgrade=list(models.AllClassGrade.objects.filter(test=test_id).values())
                    avgclass=list(models.AllTest.objects.filter(TesT_id=test_id).values())

                    target_sub=models.ClassGrade.objects.values(sub_key).filter(TEST_id=test_id)
                    print(target_sub)
                    for i in list(target_sub):
                        if i.get(sub_key)<=70:
                            grade_5+=1
                        if 70<i.get(sub_key)<=80:
                            grade_t+=1
                        if 80<i.get(sub_key)<=90:
                            grade_4+=1
                        if 90<i.get(sub_key)<=100:
                            grade_3+=1
                        if 100<i.get(sub_key)<=110:
                            grade_2+=1
                        if 110<i.get(sub_key)<=130:
                            grade_1+=1
                        if 130<i.get(sub_key)<=150:
                            grade_0+=1

                    pass_grade=models.ClassGrade.objects.values(sub_key).filter(TEST_id=test_id)
                    for i in list(pass_grade):
                        if i.get(sub_key)>=max_score*0.6:
                            pass_1+=1
                        if i.get(sub_key)<max_score*0.6:
                            unpass_1+=1
                    pass_grade=models.ClassGrade.objects.values(sub_key).filter(TEST_id=int(test_id)-1)
                    for i in list(pass_grade):
                        if i.get(sub_key)>=max_score*0.6:
                            pass_2+=1
                        if i.get(sub_key)<max_score*0.6:
                            unpass_2+=1
                    pass_grade=models.ClassGrade.objects.values(sub_key).filter(TEST_id=int(test_id)-2)
                    for i in list(pass_grade):
                        if i.get(sub_key)>=max_score*0.6 :
                            pass_3+=1
                        if i.get(sub_key)<max_score*0.6 :
                            unpass_3+=1
                
                    #预测部份
                    x,y=Pretreatment(grade_final,sub_key,max_score)
                    pre_model=pm.predict_model()
                    pre_model.set_train(x,y)
                    final_score,optimal=pre_model.get_res([5,float(hard)])
                    final_score=final_score*(max_score/100)
                    cost=pre_model.cost_function()
                    grademin=int(final_score-cost/10)
                    if int(final_score+cost/10)<=150:
                        grademax=int(final_score+cost/10)
                    else:
                        grademax=150
                
                    message_tx='预测完成'
                    res=1
                    if models.ClassGrade.objects.values(sub_key).count()<=30:
                        message='本次预测数据小于30个，模型可信度<1%'
                    else :
                        if 80>models.ClassGrade.objects.values(sub_key).count()>30:
                            message='本次预测数据介于30-80个，模型可信度接近15%'
                        else:
                            if 200>models.ClassGrade.objects.values(sub_key).count()>80:
                                message='本次预测数据介于80-200个，模型可信度接近60%'
                            else:
                                message='本次预测数据大于200个，模型可信度到达70%以上'
                    #普通数据
                else:
                    message_tx='无此班数据'
            
        else:
            message_tx='传参错误'
        
    return render(
        request,
        'app/subject_predict.html',
        {
            'title':'科目预测/Predict',
            'message':'Predict page.',
            'year':datetime.now().year,
            'message':message_tx,
            'premessage':message,
            'res':res,
            'score':int(final_score),
            'theta1':float(optimal[0]),
            'theta2':float(optimal[1]),
            'theta3':float(optimal[2]),
            'grademin':grademin,
            'grademax':grademax,
            'max_score':max_score,
            'subname':sub_name,
            'testid':test_id,
            'avgclass':avgclass,
            'avgall':allgrade,
            'grade_fir':grade_1,
            'grade_sec':grade_2,
            'grade_thr':grade_3,
            'grade_four':grade_4,
            'grade_fiv':grade_5,
            'grade_zero':grade_0,
            'grade_temp':grade_t,
            'pass1':pass_1,
            'unpass1':unpass_1,
            'pass2':pass_2,
            'unpass2':unpass_2,
            'pass3':pass_3,
            'unpass3':unpass_3,
        }
    )

def class_analysis(request):
    """Renders the analysis page."""
    assert isinstance(request, HttpRequest)
    res,message,class_id,test_id='','','',''
    teacher_class=[]
    max_grade,min_grade,avg_grade,in2_count=[],[],[],[]
    test_id_temp=[]
    lastin200,max_min,trend='','',''
    try:
        teacher_class.append(request.user.TeacherClass)
    except:
        teacher_class.append(4)
    if request.method =="POST":
        class_id=request.POST.get('class')
        if class_id:
            target=models.ClassGrade.objects.filter(CLASS=class_id)
            if target:
                test_id=list(models.AllTest.objects.filter(Class=class_id).values('TesT_id').order_by('TesT_id'))
                for i in test_id:
                    temp=models.ClassGrade.objects.filter(TEST_id=i.get('TesT_id')).order_by('-Total').values()
                    if list(temp):
                        max_grade.append(list(temp)[0].get('Total'))
                    temp=models.ClassGrade.objects.filter(TEST_id=i.get('TesT_id')).order_by('Total').values()
                    if list(temp):
                        min_grade.append(list(temp)[0].get('Total'))
                    temp=models.AllTest.objects.filter(TesT_id=i.get('TesT_id')).values()
                    if list(temp):
                        avg_grade.append(list(temp)[0].get('total'))
                    temp=models.ClassGrade.objects.filter(TEST_id=i.get('TesT_id')).order_by('-Total').values()
                    count=0
                    for j in list(temp)[:200]:
                        if j.get('CLASS')==class_id:
                            count+=1
                    in2_count.append(count)
                res=1
                try:
                    lastin200=in2_count[-1]
                except:
                    lastin200='无'
                try:
                    max_min=max_grade[-1]-min_grade[-1]
                except:
                    max_min='无数据'
                try:
                    if avg_grade[-1]-avg_grade[-2]>=0:
                        trend='上升'
                    else:
                        trend='下降'
                except:
                    trend='无法判断'
                test_id=[int(i.get('TesT_id')) for i in list(models.AllTest.objects.filter(Class=class_id).values('TesT_id').order_by('TesT_id'))]
            else:
                message='此班无数据!'
        else:
            message='传参错误，请检查!'
    return render(
        request,
        'app/class_analysis.html',
        {
            'title':'班级分析/Analysis',
            'message':'Analysis page.',
            'year':datetime.now().year,
            'res':res,
            'anmessage':message,
            'tcclass':teacher_class,
            'class':class_id,
            'testcount':test_id,
            'max_grade':max_grade,
            'min_grade':min_grade,
            'avg_grade':avg_grade,
            'in200':in2_count,
            'trend':trend,
            'lastin200':lastin200,
            'max_min':max_min,
        }
    )

def subject_analysis(request):
    """Renders the analysis page."""
    assert isinstance(request, HttpRequest)
    class_id,test_id,rank='','',''
    trend,avg_grade,max_in5,min_in5,max_math,max_chinese,max_english,max_bio,max_che,max_phy=0,'','','','','','','','',''
    teacher_class=[]
    try:
        teacher_class.append(request.user.TeacherClass)
    except:
        teacher_class.append(4)
    #获取所有班级的所有次考试，得到最近考试次数
    class_all_full_prime=models.AllTest.objects.filter(Class=teacher_class[0]).values()
    class_testid=[int(i.get('TesT_id')) for i in list(class_all_full_prime)]
    now_testid=max(class_testid)

    #获取顺位并处理
    class_rank=class_all_full_prime.filter(TesT_id=now_testid).order_by('total')
    temp=0
    for i in class_rank:
        temp+=1
        if i.get('Class')==teacher_class[0]:
            rank=temp
        else:
            rank='error'
            temp=0
    avg_grade_prime=models.AllTest.objects.filter(Class=teacher_class[0],TesT_id=now_testid).values()
    if avg_grade_prime:
        avg_grade=list(avg_grade_prime)[0].get('total')
    else:
        avg_grade='error'
    #获得当前班级的所有次数考试，将其打包为各学科值
    class_all_full=models.AllTest.objects.filter(Class=teacher_class[0]).values().order_by('TesT_id')
    class_all=list(class_all_full)
    #获取趋势并计算
    class_total=[int(i.get('total')) for i in list(class_all)]
    if len(class_total)>=2:
        trend=int(((class_total[-1]-class_total[-2])/class_total[-2])*100)
    else:
        trend=0
    if trend>=0:
        trend='+'+str(trend)
    else:
        trend='-'+str(trend)

    grade_prime=models.ClassGrade.objects.filter(CLASS=teacher_class[0],TEST_id=now_testid)
    max_math_prime=grade_prime.order_by('-Math3').values()
    max_math=list(max_math_prime)[0]
    max_chinese_prime=grade_prime.order_by('-Chinese3').values()
    max_chinese=list(max_chinese_prime)[0]
    max_eng_prime=grade_prime.order_by('-English3').values()
    max_english=list(max_eng_prime)[0]
    max_bio_prime=grade_prime.order_by('-Biology3').values()
    max_bio=list(max_bio_prime)[0]
    max_che_prime=grade_prime.order_by('-Chemistry3').values()
    max_che=list(max_che_prime)[0]
    max_phy_prime=grade_prime.order_by('-Physics3').values()
    max_phy=list(max_phy_prime)[0]

    max_in5=list(grade_prime.order_by('-Total').values())[:5]
    min_in5=list(grade_prime.order_by('Total').values())[:5]
    return render(
        request,
        'app/subject_analysis.html',
        {
            'title':'学况速览/Analysis',
            'message':'Analysis page.',
            'year':datetime.now().year,
            'rank':rank,
            'class':teacher_class,
            'trend':trend,
            'avg_grade':avg_grade,
            'max_in5':max_in5,
            'min_in5':min_in5,
            'max_math':max_math,
            'max_chinese':max_chinese,
            'max_english':max_english,
            'max_bio':max_bio,
            'max_che':max_che,
            'max_phy':max_phy,
        }
    )

def register(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/register.html',
        {
            'title':'注册',
            'year':datetime.now().year,
        }
    )

def page_not_found(request,exception,template_name='error/404.html'):
    
    return render(request,template_name)

def page_error(request,template_name='error/500.html'):
    #404
    return render(request,template_name)

def permission_denied(request,exception,template_name='error/403.html'):
    #403
    return render(request, template_name)

def bad_request(request,exception,template_name='error/400.html'):
    #400
    return render(request, temptale_name)

def Pretreatment(data,target,full):
    x1=[int(i.get('TEST_id')) for i in data]
    y=[i.get(str(target)) for i in data]
    x2=[]
    temp1=[]
    temp2=[]
    temp3=[]
    xy=list(zip(x1,y))
    max_id=max([i[0] for i in xy])
    for i in range(max_id):
        y_same=[]
        count=0
        for j in xy:
            if i+1==j[0]:
                y_same.append(j[1])
                count+=1
        for _ in range(count):
            x2.append(hardrank(y_same,full))
    for i in x1:
        temp1.append([i-int(max_id)+4])
    for j in x2:
        temp2.append([j])
    for i in y:
        i=(i/full)*100
        temp3.append([i])
    y=temp3
    x=np.hstack((temp1,temp2))
    return x,y
        
def hardrank(y,full):
    temp=0
    for i in y:
        temp+=i
    avg=temp/len(y)
    return 1-avg/full

def subjects(sub_name):
    max_score=0
    sub_key=''
    if sub_name=='数学':
        sub_key='Math3'
        max_score=150
    if sub_name=='语文':
        sub_key='Chinese3'
        max_score=150
    if sub_name=='英语':
        sub_key='English3'
        max_score=150
    if sub_name=='生物':
        sub_key='Biology3'
        max_score=90
    if sub_name=='化学':
        sub_key='Chemistry3'
        max_score=100
    if sub_name=='物理':
        sub_key='Physics3'
        max_score=110
    return max_score,sub_key
