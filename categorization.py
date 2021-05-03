# -*- coding: utf-8 -*-
# Created on Sat Nov  7 14:31:17 2020   @author: fan

import pandas as pd                         # for data
import plotly.express as px                 # scatter 3D - px.scatter_3d
import plotly.graph_objects as go           # html
#import plotly.figure_factory as ff          # quiver
#import matplotlib.pyplot as plt             # classic 3D

def get_range(gdata, fkeys):
    grange = [ [ gdata[[fkeys[4]]].values.min()-1, \
                gdata[[fkeys[4]]].values.max()+1 ], \
               [ gdata[[fkeys[5]]].values.min()-1, \
                gdata[[fkeys[5]]].values.max()+1 ], \
               [ gdata[[fkeys[6]]].values.min()-1, \
                gdata[[fkeys[6]]].values.max()+1 ] ]  # set min, max of axis
    return grange

def plot_plotly_point(pdata, fkeys, prange, prow):
    sizer = 0 # all points are same size
    fdia = [min(pdata[fkeys[4+sizer]]), max(pdata[fkeys[4+sizer]])] 
    #pdata["diameter"] = (pdata[fkeys[3+sizer]]-fdia[0])/(fdia[1]-fdia[0])*9+1
    # figure, point, text, title # size="diameter", size_max=50
    fig = px.scatter_3d(pdata, x=fkeys[4],y=fkeys[5],z=fkeys[6],text=fkeys[1], \
                        color=fkeys[0], title=prow)
    fig.update_traces(textposition='middle right', selector=dict(type='scatter3d')) # set the text position
    fig.add_traces(go.Scatter3d(x=prange[0], y=[0,0], z=[0,0],
                              mode='lines',
                              line_width=6,
                              #textposition='middle right',
                              name='Axis of Time'))
    fig.add_traces(go.Scatter3d(x=[0,0], y=prange[1], z=[0,0],
                              mode='lines',
                              line_width=6,
                              name='Axis of Space'))
    fig.add_traces(go.Scatter3d(x=[0,0], y=[0,0], z=prange[2],
                              mode='lines',
                              line_width=6,
                              name='Axis of Quantity'))
    fig.add_traces(go.Cone(
        x = [prange[0][1]+1, 0, 0],
        y = [0, prange[1][1]+1, 0],
        z = [0, 0, prange[2][1]+1],
        u = [1, 0, 0],
        v = [0, 1, 0],
        w = [0, 0, 1],
    #sizemode = "absolute",
    autocolorscale = False,
    sizeref = 0.1,
    #coloraxis=None, colorbar = None, colorscale=None, showlegend=False,
    showscale=False, 
    anchor = "tip") )
    return fig

def plot_plotly_bubble(pdata, fkeys, prange, prow, ptype, nxyz): # not in use
    pdia = "diameter"
    fdia = [min(pdata[fkeys[4+nxyz[2]]]), max(pdata[fkeys[4+nxyz[2]]])]
    pdata[pdia] = (pdata[fkeys[4+nxyz[2]]]-fdia[0])/(fdia[1]-fdia[0])*9+1
    fig = px.scatter(pdata, x=fkeys[4+nxyz[0]], y=fkeys[4+nxyz[1]], \
                     size=pdia, color=fkeys[0], text=fkeys[1], \
                         opacity=0.5, hover_name=fkeys[1], size_max=50)
    fig.write_html('figure_'+prow+'_'+ptype+'_'+str(nxyz[2])+'.html', \
                   auto_open=True) # export
    return fig

def get_table_val(tdatai, tkeys, tvalue, ttype, tview):
    # get table
    tdata0 = tdatai.loc[(tdatai[tkeys[3]]==tvalue[0])]  # get rows
    tdata0 = tdata0[[tkeys[0], tkeys[1], tkeys[4], tkeys[5], tkeys[6]]]    # get cols
    # calculate range
    tdata0range = tdata0.fillna(0)                      # fill 0
    trange = get_range(tdata0range, tkeys)              # get range
    # plot
    if "scatter" == ttype:
        tfig = plot_plotly_point(tdata0, tkeys, trange, tvalue[0])  # plot
    #if "bubble" == ttype: # not in use
    #    tfig = plot_plotly_bubble(tdata0, tkeys, trange, tvalue[0], ttype, tview) # not in use
    return tdata0, tfig, trange                         # return

def plot_plotly_arrow(pdata, pa, pb, pc, pkeys, pfig):
    # create line from 1 to 2
    for row in pdata.itertuples():
        pfig.add_traces(go.Scatter3d(x=[row.ax, row.cx, row.bx],
                                     y=[row.ay, row.cy, row.by],
                                     z=[row.az, row.cz, row.bz],
                              mode='lines+text',
                              text=['',row._1,''],
                              line_width=3,
                              #showlegend=False,
                              name=row._1)) # not robust -> ax ay az bx by bz _1
    # create cone from 1 to 2
    ua = pdata[[pb[0]]].values.transpose()[0] - pdata[[pa[0]]].values.transpose()[0]
    va = pdata[[pb[1]]].values.transpose()[0] - pdata[[pa[1]]].values.transpose()[0]
    wa = pdata[[pb[2]]].values.transpose()[0] - pdata[[pa[2]]].values.transpose()[0]
    pfig.add_traces( go.Cone(
        x = pdata[[pb[0]]].values.transpose()[0].tolist(),
        y = pdata[[pb[1]]].values.transpose()[0].tolist(),
        z = pdata[[pb[2]]].values.transpose()[0].tolist(),
        u = ua.tolist(),
        v = va.tolist(),
        w = wa.tolist(),
        sizemode = "absolute",
        sizeref = 0.5,
        autocolorscale = False,
        showscale=False, 
        anchor = "tip") )
    return pfig

def get_table_equ(tdatai, tkeys, tvalue, tfig):
    # get table
    tdata2 = tdatai.loc[(tdatai[tkeys[3]]==tvalue[0])]  # get rows
    tdata0 = tdatai.loc[(tdatai[tkeys[3]]==tvalue[1])]  # get rows
    tdata1 = tdata0[[tkeys[0], tkeys[1], tkeys[2], tkeys[4], tkeys[5], tkeys[6]]]    # get cols
    # fill points A to rows
    ta = ["ax", "ay", "az"]
    tdata1[ta[0]] = tdata1[tkeys[1]].apply(lambda x:tdata2.loc[ tdata2[ tkeys[1] ] ==x][[tkeys[4]]].values[0,0])
    tdata1[ta[1]] = tdata1[tkeys[1]].apply(lambda x:tdata2.loc[ tdata2[ tkeys[1] ] ==x][[tkeys[5]]].values[0,0])
    tdata1[ta[2]] = tdata1[tkeys[1]].apply(lambda x:tdata2.loc[ tdata2[ tkeys[1] ] ==x][[tkeys[6]]].values[0,0])
    # fill points B to rows
    tb = ["bx", "by", "bz"]
    tdata1[tb[0]] = tdata1[tkeys[2]].apply(lambda x:tdata2.loc[ tdata2[ tkeys[1] ] ==x][[tkeys[4]]].values[0,0])
    tdata1[tb[1]] = tdata1[tkeys[2]].apply(lambda x:tdata2.loc[ tdata2[ tkeys[1] ] ==x][[tkeys[5]]].values[0,0])
    tdata1[tb[2]] = tdata1[tkeys[2]].apply(lambda x:tdata2.loc[ tdata2[ tkeys[1] ] ==x][[tkeys[6]]].values[0,0])
    # fill points C 1/3 to rows
    tc = ["cx", "cy", "cz"]
    tdata1[tc[0]] = tdata1[ta[0]] + (tdata1[tb[0]] - tdata1[ta[0]])/2
    tdata1[tc[1]] = tdata1[ta[1]] + (tdata1[tb[1]] - tdata1[ta[1]])/2
    tdata1[tc[2]] = tdata1[ta[2]] + (tdata1[tb[2]] - tdata1[ta[2]])/2
    # plot rows with A, B, C
    tfig = plot_plotly_arrow(tdata1, ta, tb, tc, tkeys, tfig)   # plot
    return tdata1, tfig # return table, figure, range

if __name__=="__main__":
    # data
    fsheetfile = "../category_data.xlsx"                # sheet file name
    fsheetname = "v5_210407"                            # sheet label name
    fhead = [0]                                         # head rows
    fkeys = ["subject small", "object 1", "object 2", "class", \
             "t(lgs)", "d(lgm)", "n(lg-)"]     # 0-3, 4-6
    fvalue = ["value", "equ"]
    fdatai = pd.read_excel(fsheetfile, sheet_name=fsheetname, header=fhead)
    # plot 3d
    fdata1, ffig1, frange1 = get_table_val(fdatai,fkeys,fvalue,"scatter",[-1,-1,-1])    # scatter
    fdata2, ffig2 = get_table_equ(fdatai,fkeys,fvalue, ffig1)                  # arrow
    ffig2.write_html('figure_'+'arrow'+'.html',auto_open=True) # export
    # plot 2d
    #fdata7, ffig7, frange7 = get_table_val(fdatai,fkeys,fvalue[0],"bubble",[0,1,2])
    #fdata8, ffig8, frange8 = get_table_val(fdatai,fkeys,fvalue[0],"bubble",[1,2,0])
    #fdata9, ffig9, frange9 = get_table_val(fdatai,fkeys,fvalue[0],"bubble",[0,2,1])