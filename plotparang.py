# Christopher A. Hales
# 2 June 2016
#
# Plot parallactic angle vs hour angle
#      and its derivative
#
# (PA = angle between line of constant
#  RA and zenith at source, measured
#  positive N through E.  For source
#  dec less than observatory latitude,
#  parallactic angle starts negative
#  as source rises in east at negative
#  HA, becomes positive as source sets
#  in west at positive HA.)
#

################################################

# latitude of observatory in degrees (+N,-S)
#obsname = 'VLA'
#lat     = 34.0784
obsname = 'ALMA'
lat     = -23.023

# lower and upper elevation limits in degrees
el_limit_lower = 10
el_limit_upper = 80

################################################

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm

pi  = np.pi
d2r = pi/180.

ha      = np.linspace(0.001,12,300)
pltindx = np.searchsorted(ha,1.1)

dec = np.arange(-80,90,20)
dec = np.append(dec,np.floor(lat/5.)*5)
dec = np.append(dec,np.floor(lat/5.)*5-5)
dec = np.append(dec,np.floor(lat/5.)*5-10)
dec = np.append(dec,np.floor(lat/5.)*5-15)
dec = np.append(dec,np.ceil(lat/5.)*5)
dec = np.append(dec,np.ceil(lat/5.)*5+5)
dec = np.append(dec,np.ceil(lat/5.)*5+10)
dec = np.append(dec,np.ceil(lat/5.)*5+15)
dec = np.unique(dec)
dec = dec[np.abs(dec)<=90]

# http://matplotlib.org/examples/color/
#        colormaps_reference.html
color = iter(cm.cool(np.linspace(0,1,len(dec))))

'''
    equations:
    http://www.gb.nrao.edu/~rcreager/GBTMetrology/
           140ft/l0058/gbtmemo52/memo52.html
'''

# parallactic angle

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
for d in range(dec.size):
    p = np.arctan2(np.sin(ha*15.*d2r) , \
        (np.tan(lat*d2r)*np.cos(dec[d]*d2r) - \
         np.sin(dec[d]*d2r)*np.cos(ha*15.*d2r)))/d2r
    el = np.arcsin(np.sin(dec[d]*d2r)*\
         np.sin(lat*d2r) + np.cos(dec[d]*d2r)*\
         np.cos(lat*d2r)*np.cos(ha*15.*d2r))/d2r
    indx1 = np.where((el>=el_limit_lower)&\
                     (el<=el_limit_upper))
    indx2 = np.where((el>=el_limit_lower)&\
                     (el>el_limit_upper))
    c = next(color)
    #c = '0.25'
    if indx1[0].size > 0:
        plt.plot(ha[indx1],p[indx1],color=c)
        plt.plot(ha[indx2],p[indx2],color=c,\
                 linestyle='--')
        plt.text(ha[pltindx],p[pltindx]-1,\
                 '{:.0f}'.format(dec[d])+'$^\circ$',\
                 weight='bold',fontsize=12)

# lower elevation limit (blue)
az   = np.linspace(0.01,360.01,361)
dec1 = np.arcsin(np.cos(az*d2r)*np.cos(lat*d2r)*\
                 np.cos(el_limit_lower*d2r)+\
                 np.sin(lat*d2r)*\
                 np.sin(el_limit_lower*d2r))
ha1 = np.arccos((np.sin(el_limit_lower*d2r) - \
      np.sin(lat*d2r)*np.sin(dec1))/\
      (np.cos(lat*d2r)*np.cos(dec1)))
p = np.arctan2(np.sin(ha1),\
              (np.cos(dec1)*np.tan(lat*d2r) -\
               np.sin(dec1)*np.cos(ha1)))/d2r
plt.plot(ha1/d2r/15.,p,color='blue',linewidth='2')

# upper elevation limit (red)
dec1 = np.arcsin(np.cos(az*d2r)*np.cos(lat*d2r)*\
                 np.cos(el_limit_upper*d2r)+\
                 np.sin(lat*d2r)*\
                 np.sin(el_limit_upper*d2r))
ha1 = np.arccos((np.sin(el_limit_upper*d2r) - \
      np.sin(lat*d2r)*np.sin(dec1))/\
      (np.cos(lat*d2r)*np.cos(dec1)))
p = np.arctan2(np.sin(ha1),\
              (np.cos(dec1)*np.tan(lat*d2r) -\
               np.sin(dec1)*np.cos(ha1)))/d2r
plt.plot(ha1/d2r/15.,p,color='red',linewidth='2')

ax.grid()
ax.set_xlim([0,12])
ax.set_ylim([0,180])
ax.set_title('Declinations viewed from '+obsname+' (lat = '+\
             '{:.1f}'.format(lat)+'$^{\!\circ\!}$)\n'+
             '(negate parallactic angle for negative HA)',\
             y=1.025,fontsize=17)
ax.set_xlabel('Hour Angle [h]',fontsize=17,labelpad=8)
ax.set_ylabel('Parallactic Angle [deg]',\
               labelpad=10,fontsize=17)
plt.xticks(range(13))
if lat >= 0:
    y_text = 152
else:
    y_text = 52

plt.text(11,y_text,'upper elevation limit = '+\
         '{:.0f}'.format(el_limit_upper)+'$^{\!\circ}$',\
         fontsize=15,color='red',ha='right')
plt.text(11,y_text-10,'lower elevation limit = '+\
         '{:.0f}'.format(el_limit_lower)+'$^{\!\circ}$',\
         fontsize=15,color='blue',ha='right')
plt.tight_layout()
#plt.show()
plt.savefig('parang_'+obsname+'.png')
plt.close()


# derivative of PA wrt HA
# (separate code for clarity)

color = iter(cm.cool(np.linspace(0,1,len(dec))))
ha2 = ha[:-1]
fig = plt.figure()
ax  = fig.add_subplot(1,1,1)
for d in range(dec.size):
    p  = np.arctan2(np.sin(ha*15.*d2r) , \
         (np.tan(lat*d2r)*np.cos(dec[d]*d2r) - \
          np.sin(dec[d]*d2r)*np.cos(ha*15.*d2r)))/d2r
    dp = np.nan_to_num(np.diff(p)/np.diff(ha*60.))
    el = np.arcsin(np.sin(dec[d]*d2r)*\
         np.sin(lat*d2r) + np.cos(dec[d]*d2r)*\
         np.cos(lat*d2r)*np.cos(ha2*15.*d2r))/d2r
    indx1 = np.where((el>=el_limit_lower)&\
                     (el<=el_limit_upper))
    indx2 = np.where((el>=el_limit_lower)&\
                     (el>el_limit_upper))
    c = next(color)
    #c = '0.25'
    if indx1[0].size > 0:
        plt.plot(ha2[indx1],dp[indx1],color=c)
        plt.plot(ha2[indx2],dp[indx2],color=c,\
                 linestyle='--')
        #plt.text(ha2[pltindx],dp[pltindx]-1,\
        #         '{:.0f}'.format(dec[d])+'$^\circ$',\
        #         weight='bold',fontsize=12)

# lower elevation limit (blue)
az   = np.linspace(-0.1,360.1,361)
dec1 = np.arcsin(np.cos(az*d2r)*np.cos(lat*d2r)*\
                 np.cos(el_limit_lower*d2r)+\
                 np.sin(lat*d2r)*\
                 np.sin(el_limit_lower*d2r))
ha1 = np.arccos((np.sin(el_limit_lower*d2r) - \
      np.sin(lat*d2r)*np.sin(dec1))/\
      (np.cos(lat*d2r)*np.cos(dec1)))
p1 = np.arctan2(np.sin(ha1),\
               (np.cos(dec1)*np.tan(lat*d2r) -\
                np.sin(dec1)*np.cos(ha1)))/d2r
ha2 = ha1+0.01
p2 = np.arctan2(np.sin(ha2),\
               (np.cos(dec1)*np.tan(lat*d2r) -\
                np.sin(dec1)*np.cos(ha2)))/d2r
dp = (p2-p1) / (0.01/d2r/15.*60.)
# hack to avoid spurious point near ha=12 at low lat
plt.plot(ha1[dp>-1.5]/d2r/15.,dp[dp>-1.5],\
         color='blue',linewidth='2')

# upper elevation limit (red)
dec1 = np.arcsin(np.cos(az*d2r)*np.cos(lat*d2r)*\
                 np.cos(el_limit_upper*d2r)+\
                 np.sin(lat*d2r)*\
                 np.sin(el_limit_upper*d2r))
ha1 = np.arccos((np.sin(el_limit_upper*d2r) - \
      np.sin(lat*d2r)*np.sin(dec1))/\
      (np.cos(lat*d2r)*np.cos(dec1)))
p1 = np.arctan2(np.sin(ha1),\
               (np.cos(dec1)*np.tan(lat*d2r) -\
                np.sin(dec1)*np.cos(ha1)))/d2r
ha2 = ha1+0.01
p2 = np.arctan2(np.sin(ha2),\
               (np.cos(dec1)*np.tan(lat*d2r) -\
                np.sin(dec1)*np.cos(ha2)))/d2r
dp = (p2-p1) / (0.01/d2r/15.*60.)
plt.plot(ha1/d2r/15.,dp,color='red',linewidth='2')

ax.grid()
ax.set_xlim([0,12])
ax.set_ylim([-1.5,1.5])
ax.set_title('Declinations viewed from '+obsname+' (lat = '+\
             '{:.1f}'.format(lat)+'$^{\!\circ\!}$)\n'+
             '(negate derivative for negative HA)',\
             y=1.025,fontsize=17)
ax.set_xlabel('Hour Angle [h]',fontsize=17,labelpad=8)
ax.set_ylabel('Par. Angle Derivative wrt. HA [deg/min]',\
               labelpad=10,fontsize=17)
plt.xticks(np.linspace(0,12,13))
#plt.yticks(np.linspace(-1.5,1.5,13))
y_text = -0.7
plt.text(11,y_text,'upper elevation limit = '+\
         '{:.0f}'.format(el_limit_upper)+'$^{\!\circ}$',\
         fontsize=15,color='red',ha='right')
plt.text(11,y_text-0.15,'lower elevation limit = '+\
         '{:.0f}'.format(el_limit_lower)+'$^{\!\circ}$',\
         fontsize=15,color='blue',ha='right')
plt.tight_layout()
#plt.show()
plt.savefig('parang_deriv_'+obsname+'.png')
plt.close()
