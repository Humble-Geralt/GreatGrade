from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    TeacherID = models.CharField('员工号', max_length=15)
    TeacherClass = models.CharField('管理班级号', max_length=15)


class Meta:
    permissions = (
        ('add_user_per', '添加用户权限'),
        ('del_user_per', '删除用户权限'),
        ('change_user_per', '修改用户权限'),
        ('sel_user_per', '查询用户权限')
    )


class ClassGrade(models.Model):  # 某次考试个人成绩，下面为各个学生成绩
    studentNum = models.CharField('学号', max_length=15)
    CLASS = models.CharField('班级', max_length=15)
    STName = models.CharField('姓名', max_length=20)
    Math3 = models.PositiveIntegerField('数学', blank=True, null=True)  # positiveintergerfield 数据大于0
    Chinese3 = models.PositiveIntegerField('语文', blank=True, null=True)
    English3 = models.PositiveIntegerField('英语', blank=True, null=True)
    Physics3 = models.PositiveIntegerField('物理', blank=True, null=True)
    Biology3 = models.PositiveIntegerField('生物', blank=True, null=True)
    Chemistry3 = models.PositiveIntegerField('化学', blank=True, null=True)
    TEST = models.ForeignKey('AllTest', on_delete=models.CASCADE)
    Total = models.PositiveIntegerField('总分', blank=True, null=True)


class Meta:
    constraints1 = [
        models.UniqueConstraint(fields=['studentNum', 'TEST'], name='unique_student'),
        models.CheckConstraint(check=models.Q(Math3__lte=150), name='Math3_lte_150'),
        models.CheckConstraint(check=models.Q(Chinese3__lte=150), name='Chinese3_lte_150'),
        models.CheckConstraint(check=models.Q(English3__lte=150), name='English3_lte_150'),
        models.CheckConstraint(check=models.Q(Physics3__lte=150), name='Physics3_lte_150'),
        models.CheckConstraint(check=models.Q(Biology3__lte=150), name='Biology3_lte_150'),
        models.CheckConstraint(check=models.Q(Chemistry3__lte=150), name='Chemistry3_lte_150')
    ]

class AllTest(models.Model):  # 各个班级各次考试人均分
    Class = models.CharField('班级', max_length=15)
    TesT = models.ForeignKey('AllClassGrade', on_delete=models.CASCADE)
    ClassTest = models.CharField('班级考试', primary_key=True, max_length=20)
    Math2 = models.PositiveIntegerField('数学', blank=True, null=True)  # positiveintergerfield 数据大于0
    Chinese2 = models.PositiveIntegerField('语文', blank=True, null=True)
    English2 = models.PositiveIntegerField('英语', blank=True, null=True)
    Physics2 = models.PositiveIntegerField('物理', blank=True, null=True)
    Biology2 = models.PositiveIntegerField('生物', blank=True, null=True)
    Chemistry2 = models.PositiveIntegerField('化学', blank=True, null=True)
    total = models.PositiveIntegerField('总分', blank=True, null=True)


class Meta:
    constraints2 = [
        models.UniqueConstraint(fields=['studentNum', 'TEST'], name='unique_student'),
        models.CheckConstraint(check=models.Q(Math2__lte=150), name='Math2_lte_150'),
        models.CheckConstraint(check=models.Q(Chinese2__lte=150), name='Chinese2_lte_150'),
        models.CheckConstraint(check=models.Q(English2__lte=150), name='English2_lte_150'),
        models.CheckConstraint(check=models.Q(Physics2__lte=150), name='Physics2_lte_150'),
        models.CheckConstraint(check=models.Q(Biology2__lte=150), name='Biology2_lte_150'),
        models.CheckConstraint(check=models.Q(Chemistry2__lte=150), name='Chemistry2_lte_150')
    ]


class AllClassGrade(models.Model):  # 年级各次考试平均分
    test = models.CharField('考试', primary_key=True, max_length=20)
    Math1 = models.PositiveIntegerField('数学', blank=True, null=True)  # positiveintergerfield 数据大于0
    Chinese1 = models.PositiveIntegerField('语文', blank=True, null=True)
    English1 = models.PositiveIntegerField('英语', blank=True, null=True)
    Physics1 = models.PositiveIntegerField('物理', blank=True, null=True)
    Biology1 = models.PositiveIntegerField('生物', blank=True, null=True)
    Chemistry1 = models.PositiveIntegerField('化学', blank=True, null=True)
    TOTAL = models.PositiveIntegerField('总分', blank=True, null=True)


class Meta:
    constraints3 = [
        models.UniqueConstraint(fields=['studentNum', 'TEST'], name='unique_student'),
        models.CheckConstraint(check=models.Q(Math1__lte=150), name='Math1_lte_150'),
        models.CheckConstraint(check=models.Q(Chinese1__lte=150), name='Chinese1_lte_150'),
        models.CheckConstraint(check=models.Q(English1__lte=150), name='English1_lte_150'),
        models.CheckConstraint(check=models.Q(Physics1__lte=150), name='Physics1_lte_150'),
        models.CheckConstraint(check=models.Q(Biology1__lte=150), name='Biology1_lte_150'),
        models.CheckConstraint(check=models.Q(Chemistry1__lte=150), name='Chemistry1_lte_150')
    ]
