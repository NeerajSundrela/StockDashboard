from flask import Flask, render_template
from markupsafe import escape
from werkzeug.exceptions import abort

app=Flask(__name__)


@app.route('/plot/')
def plot():
    from pandas_datareader import data
    from bokeh.plotting import figure, output_file, show
    import datetime
    from bokeh.embed import components
    from bokeh.resources import CDN

    def inc_or_dec(c,o):
        if c>o:
            value='Increase'
        elif c<o:
            value='Decrease'
        else:
            value='Equal'
        return value



    start=datetime.datetime(2019,12,31)
    end=datetime.datetime(2020,4,16)
    df = data.DataReader(name="GOOG",data_source="yahoo",start=start,end=end)

    df['Status']=[inc_or_dec(c,o) for c,o in zip(df.Close,df.Open)]
    df['Middle']=(df.Open+df.Close)/2
    df['Height']=abs(df.Close-df.Open)

    p=figure(x_axis_type='datetime',width=600,height=180,sizing_mode='scale_width')
    p.title.text="CandleStick Figure"
    p.grid.grid_line_alpha=0.4

    hour_12=12*60*60*1000

    # p.rect(df.index[df.Close>df.Open],(df.Open+df.Close)/2,hour_12,abs(df.Open-df.Close),
    # fill_color='lightblue',line_color='black')
    # p.rect(df.index[df.Open>df.Close],(df.Open+df.Close)/2,hour_12,abs(df.Open-df.Close),
    # fill_color='red',line_color='black')

    p.segment(df.index,df.High,df.index,df.Low,color='black')
    p.rect(df.index[df.Status=='Increase'],df.Middle,hour_12,df.Height,
    fill_color='lightblue',line_color='black')
    p.rect(df.index[df.Status=='Decrease'],df.Middle,hour_12,df.Height,
    fill_color='red',line_color='black')

    script1,div1 = components(p)
    js_script=CDN.js_files

    # output_file("out.html")

    # show(p)
    return render_template('plot.html',script1=script1,
    div1=div1,js_script=js_script[0])

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")


if __name__=='__main__':
    app.run(debug=True)