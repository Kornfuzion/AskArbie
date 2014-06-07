# Create your views here.

from django.http import HttpResponse
from django.template import RequestContext, loader
import sys

from pylab import plot, show, savefig, clf
from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq

from mysite.invest.models import User

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
        makeFig()
        context = RequestContext(request, {
            'name': usrs[0].name
        })
    return HttpResponse(template.render(context))
