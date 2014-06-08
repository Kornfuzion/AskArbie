# Create your views here.

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
import math
import sys

from pylab import plot, show, savefig, clf
from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq

from mysite.invest.models import User
from mysite.invest.models import RBC_Customer
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg

#with open('invest_sees_path', 'w') as f:
#    f.write(repr(sys.path))
#    f.write("\n\n\n")
#    f.write(repr(User))

def makeFig():
    clf()
    data = vstack((rand(150,2) + array([.5,.5]), rand(150,2)))
    centroids,_=kmeans(data, 3)
    idx,_ = vq(data, centroids)
    plot(data[idx==0,0],data[idx==0,1],'ob',
         data[idx==1,0],data[idx==1,1],'or',
         data[idx==2,0],data[idx==2,1],'og'
    )
    plot(centroids[:,0],centroids[:,1], 'sg', markersize=8)
    savefig('/home/james/mysite/media/cluster.png')


def index(request):
    with open('dump.txt', 'w') as f:
        f.write("Got HERE!")
    return HttpResponse("Hello World!")

def account(request, num):
    template = loader.get_template('invest/home.html')
    usrs = User.objects.all().filter(account_number=num)
    if (len(usrs) == 0):
        context = RequestContext(request, {})
    else:
        #makeFig()
        context = RequestContext(request, {
            'name': usrs[0].name
        })
    return HttpResponse(template.render(context))

def login(request):
    return render_to_response('invest/index.html')

def about_cluster(cluster):
    risk = math.floor(RBC_Customer.objects.all().filter(clusterID=cluster).aggregate(Avg('risk'))["risk__avg"])
    riskCategory = "Low"
    if risk > 30:
        riskCategory= "Medium"
    if risk > 60:
        riskCategory = "High"
    roi = [{"time_period":i, "value":RBC_Customer.objects.all().filter(clusterID=cluster).aggregate(Avg('roi_%s' % i))["roi_%s__avg" % i]} for i in range(1, 21)]
    income = RBC_Customer.objects.all().filter(clusterID=cluster).aggregate(Avg('income'))["income__avg"]
    return (risk, riskCategory, roi, income)

def sorted_investments(cluster):
    people = RBC_Customer.objects.all().filter(clustedID=cluster)
    investments = [[i, 0] for i in range(19)]
    for p in people:
        roi = p.roi_20
        for i in range(1,20):
            investments[i][1] += roi * getattr(p, "investmentData_%s" % (i+1))
    print "weighted", investments
    s = sorted(invesments, key=lambda x: x[1], reverse=True)
    print "sorted", s
    print "vals", [x[0] for x in s]
    return [x[0] for x in s]

def get_recommendations(customer):
    s = sorted_invesments(customer.clusterID)
    add = []
    rem = []
    for i in s[0:3]:
        if getattr(customer, "investmentData_%s" % (i+1)) == 0:
            add.append(i)
    for i in s[-3:0]:
        if getattr(customer, "investmentData_%s" % (i+1)) > 0:
            rem.append(i)
    print "add", add
    print "rem", rem
    return (add, rem)

def request_login(request):
    userid = 0
    if request.POST:
        userid = request.POST.get('account_number')
        request.session['user_id'] = userid
        try:	
            rec = RBC_Customer.objects.get(id=userid)
        except ObjectDoesNotExist:
            return render_to_response('invest/index.html')
        return display_home(request)
    else:
        return render_to_response('invest/index.html')

def edit_account(request):
    template = loader.get_template('invest/profile.html')
    if not request.session.has_key('user_id'):
	return render_to_response('invest/index.html')

    userid = request.session['user_id']
    rec = RBC_Customer.objects.get(id=userid)
    if rec is None:
        return render_to_response('invest/index.html')
    else:
        #makeFig()
        context = RequestContext(request, {
            'username': rec.userName,
            'investment_1_name': 'High Risk Stock A',
            'investment_1_value': rec.investmentData_1,
            'investment_2_name': 'High Risk Stock B',
            'investment_2_value': rec.investmentData_2,
            'investment_3_name': 'High Risk Stock C',
            'investment_3_value': rec.investmentData_3,
            'investment_4_name': 'Medium Risk Stock A',
            'investment_4_value': rec.investmentData_4,
            'investment_5_name': 'Medium Risk Stock B',
            'investment_5_value': rec.investmentData_5,
            'investment_6_name': 'Medium Risk Stock C',
            'investment_6_value': rec.investmentData_6,
            'investment_7_name': 'Low Risk Stock A',
            'investment_7_value': rec.investmentData_7,
            'investment_8_name': 'Low Risk Stock B',
            'investment_8_value': rec.investmentData_8,
            'investment_9_name': 'Low Risk Stock C',
            'investment_9_value': rec.investmentData_9,
            'investment_10_name': 'High Risk Short Term Mutual Fund',
            'investment_10_value': rec.investmentData_10,
            'investment_11_name': 'High Risk Long Term Mutual Fund',
            'investment_11_value': rec.investmentData_11,
            'investment_12_name': 'Low Risk Short Term Mutual Fund',
            'investment_12_value': rec.investmentData_12,
            'investment_13_name': 'Low Risk Long Term Mutual Fund',
            'investment_13_value': rec.investmentData_13,
            'investment_14_name': 'GIC A',
            'investment_14_value': rec.investmentData_14,
            'investment_15_name': 'GIC B',
            'investment_15_value': rec.investmentData_15,
            'investment_16_name': 'GIC C',
            'investment_16_value': rec.investmentData_16,
            'investment_17_name': 'Bond A',
            'investment_17_value': rec.investmentData_17,
            'investment_18_name': 'Bond B',
            'investment_18_value': rec.investmentData_18,
            'investment_19_name': 'Bond C',
            'investment_19_value': rec.investmentData_19,
        })

    return HttpResponse(template.render(context))

def display_home(request):
    template = loader.get_template('invest/browse.html')
    
    if not request.session.has_key('user_id'):
	return render_to_response('invest/index.html')
    
    userid=request.session['user_id']
    rec = RBC_Customer.objects.get(id=userid)
    if rec is None:
        return render_to_response('invest/index.html')
    else:
        #makeFig()
        (clusterRisk, clusterRiskCategory, clusterRoi, clusterIncome) = about_cluster(rec.clusterID)
        (add, rem) = get_recommendations(rec)
        userpoints = list()
        userpoints.append({"time_period":1, "you" :rec.roi_1, "avg":clusterRoi[0]["value"]})
        userpoints.append({"time_period":2, "you" :rec.roi_2, "avg":clusterRoi[1]["value"]})
        userpoints.append({"time_period":3, "you" :rec.roi_3, "avg":clusterRoi[2]["value"]})
        userpoints.append({"time_period":4, "you" :rec.roi_4, "avg":clusterRoi[3]["value"]})
        userpoints.append({"time_period":5, "you" :rec.roi_5, "avg":clusterRoi[4]["value"]})
        userpoints.append({"time_period":6, "you" :rec.roi_6, "avg":clusterRoi[5]["value"]})
        userpoints.append({"time_period":7, "you" :rec.roi_7, "avg":clusterRoi[6]["value"]})
        userpoints.append({"time_period":8, "you" :rec.roi_8, "avg":clusterRoi[7]["value"]})
        userpoints.append({"time_period":9, "you" :rec.roi_9, "avg":clusterRoi[8]["value"]})
        userpoints.append({"time_period":10, "you" :rec.roi_10, "avg":clusterRoi[9]["value"]})
        userpoints.append({"time_period":11, "you" :rec.roi_11, "avg":clusterRoi[10]["value"]})
        userpoints.append({"time_period":12, "you" :rec.roi_12, "avg":clusterRoi[11]["value"]})
        userpoints.append({"time_period":13, "you" :rec.roi_13, "avg":clusterRoi[12]["value"]})
        userpoints.append({"time_period":14, "you" :rec.roi_14, "avg":clusterRoi[13]["value"]})
        userpoints.append({"time_period":15, "you" :rec.roi_15, "avg":clusterRoi[14]["value"]})
        userpoints.append({"time_period":16, "you" :rec.roi_16, "avg":clusterRoi[15]["value"]})
        userpoints.append({"time_period":17, "you" :rec.roi_17, "avg":clusterRoi[16]["value"]})
        userpoints.append({"time_period":18, "you" :rec.roi_18, "avg":clusterRoi[17]["value"]})
        userpoints.append({"time_period":19, "you" :rec.roi_19, "avg":clusterRoi[18]["value"]})
        userpoints.append({"time_period":20, "you" :rec.roi_20, "avg":clusterRoi[19]["value"]})
	#print (clusterRisk, clusterRiskCategory, clusterRoi, clusterIncome)
        context = RequestContext(request, {
            'username': rec.userName,
            'investment_1_name': 'High Risk Stock A',
            'investment_1_value': round(rec.investmentData_1*100, 1),
            'investment_2_name': 'High Risk Stock B',
            'investment_2_value': round(rec.investmentData_2*100, 1),
            'investment_3_name': 'High Risk Stock C',
            'investment_3_value': round(rec.investmentData_3*100, 1),
            'investment_4_name': 'Medium Risk Stock A',
            'investment_4_value': round(rec.investmentData_4*100, 1),
            'investment_5_name': 'Medium Risk Stock B',
            'investment_5_value': round(rec.investmentData_5*100, 1),
            'investment_6_name': 'Medium Risk Stock C',
            'investment_6_value': round(rec.investmentData_6*100, 1),
            'investment_7_name': 'Low Risk Stock A',
            'investment_7_value': round(rec.investmentData_7*100, 1),
            'investment_8_name': 'Low Risk Stock B',
            'investment_8_value': round(rec.investmentData_8*100, 1),
            'investment_9_name': 'Low Risk Stock C',
            'investment_9_value': round(rec.investmentData_9*100, 1),
            'investment_10_name': 'High Risk Short Term Mutual Fund',
            'investment_10_value': round(rec.investmentData_10*100, 1),
            'investment_11_name': 'High Risk Long Term Mutual Fund',
            'investment_11_value': round(rec.investmentData_11*100, 1),
            'investment_12_name': 'Low Risk Short Term Mutual Fund',
            'investment_12_value': round(rec.investmentData_12*100, 1),
            'investment_13_name': 'Low Risk Long Term Mutual Fund',
            'investment_13_value': round(rec.investmentData_13*100, 1),
            'investment_14_name': 'GIC A',
            'investment_14_value': round(rec.investmentData_14*100, 1),
            'investment_15_name': 'GIC B',
            'investment_15_value': round(rec.investmentData_15*100, 1),
            'investment_16_name': 'GIC C',
            'investment_16_value': round(rec.investmentData_16*100, 1),
            'investment_17_name': 'Bond A',
            'investment_17_value': round(rec.investmentData_17*100, 1),
            'investment_18_name': 'Bond B',
            'investment_18_value': round(rec.investmentData_18*100, 1),
            'investment_19_name': 'Bond C',
            'investment_19_value': round(rec.investmentData_19*100, 1),
            'roiUser':userpoints,
            'clusterRisk': int(clusterRisk),
            'clusterRiskCategory': clusterRiskCategory,
            'clusterRoi': clusterRoi,
            'clusterIncome': "%.2f" % clusterIncome,
        })

    return HttpResponse(template.render(context))


