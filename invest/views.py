# Create your views here.

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
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
    risk = math.floor(RBC_Customer.objects.all().filter("clusterID"=cluster).aggregate(Avg('risk')))
    riskCategory = "Low"
    if risk > 30:
        riskCategory= "Medium"
    if risk > 60:
        riskCategory = "High"
    roi = [{"time_period":(i+1), "value":RBC_Customer.objects.all().filter("clusterID"=cluster).aggregate(Avg('roi_%s' % i))} for i in range(1, 21)]
    income = RBC_Customer.objects.all().filter("clusterID"=cluster).aggregate(Avg('income'))
    return (risk, riskCategory, roi, income)

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
        (clusterRisk, clusterRiskCategory, clusterRoi, clusterIncome) = about_cluster(rec.clusterID)
        context = RequestContext(request, {
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
            'clusterRisk': clusterRisk,
            'clusterRiskCategory': clusterRiskCategory,
            'clusterRoi': clusterRoi,
            'clusterIncome': clusterIncome,


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
        context = RequestContext(request, {
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


