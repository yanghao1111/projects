from django.db import models


# 此处的类与数据库中的表相关联
# Create your models here.
# 读者类型表
class ReaderType(models.Model):
    rdType_choices = ((0, "教师"), (1, "本科生"), (2, "专科生"), (3, "研究生"), (4, "博士生"),)
    rdType = models.CharField(max_length=10,primary_key=True,verbose_name="读者类型",choices=rdType_choices)     #读者类型  共五种（教师、本科生、专科生、研究生、博士生）
    rdTypeName = models.CharField(max_length=20, unique=True, null=False,verbose_name="读者类型名" ) #读者类别名称【唯一、非空】
    CanLendQty = models.IntegerField(verbose_name="可借书数量")  #  可借书数量
    CanLendDay = models.IntegerField(verbose_name="可借书天数")  #  可借书天数
    CanContinueTimes = models.IntegerField(verbose_name="可续借的次数")  #可续借的次数
    PunishRate=models.DecimalField(max_digits=2,decimal_places=1,verbose_name="罚款率")  #罚款率（元/天）

    def __str__(self):
        return self.rdType
# 读者表
class Reader(models.Model):
    rdID=models.CharField(primary_key=True,verbose_name="读者ID",max_length=10)
    rdName=models.CharField(max_length=20,verbose_name="读者姓名")
    rdSex_choices = (
        (1, "男"),
        (2, "女"),
    )
    def __str__(self):
        return self.rdName
    rdSex=models.IntegerField(verbose_name="读者性别",choices=rdSex_choices)
    rdType=models.SmallIntegerField(verbose_name="读者类型")
    rdDept=models.CharField(max_length=20,verbose_name="读者单位")
    rdPhone=models.CharField(max_length=11,verbose_name="读者电话")
    rdEmail=models.CharField(max_length=25,verbose_name="读者邮箱")
    rdDateReg=models.DateTimeField(verbose_name="读者登记日期")  #读者登记日期/办证日期
    rdStatus=models.CharField(max_length=2,verbose_name="状态")
    rdBorrowQty=models.IntegerField(verbose_name="可借书天数")
    rdPwd=models.CharField(max_length=25,verbose_name="密码")
    rdAdminRoles_choices = ((0, "读者"), (1, "借书证管理"), (2, "图书管理"), (4, "借阅管理"), (8, "系统管理"))
    rdAdminRoles=models.SmallIntegerField(verbose_name="权限",choices=rdAdminRoles_choices)


    rdType=models.ForeignKey(to=ReaderType,to_field="rdType",on_delete=models.CASCADE)


class Book(models.Model):
    bkID=models.IntegerField(primary_key=True,verbose_name="图书编号")
    bkCode=models.CharField(max_length=20,verbose_name="IBSN码")
    bkName=models.CharField(max_length=50,verbose_name="书名")
    def __str__(self):
        return self.bkName
    bkAuthor=models.CharField(max_length=30,verbose_name="作者")
    bkStatus=models.CharField(max_length=2,verbose_name="状态")


class Borrow(models.Model):
    BorrowID=models.IntegerField(primary_key=True,verbose_name="借书顺序号")

    rdID=models.IntegerField(verbose_name="读者ID")
    bkID=models.IntegerField(verbose_name="书籍编号")
    IdContinueTimes=models.IntegerField(verbose_name="可借阅时间")
    ldDateOut=models.DateTimeField(verbose_name="借书时间")
    ldDateRetPlan=models.DateTimeField(verbose_name="应还时间")
    ldDateRetAct=models.DateTimeField(verbose_name="实际还书日期")
    rdID=models.ForeignKey(to=Reader,to_field="rdID",on_delete=models.CASCADE)
    bkID = models.ForeignKey(to=Book, to_field="bkID", on_delete=models.CASCADE)