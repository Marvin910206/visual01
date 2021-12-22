#包成函數-1
import mplfinance as mpf
import pandas_datareader.data as web
import pyimgur
CLIENT_ID = "你的Imgur Client ID"

def plot_stcok_k_chart(CLIENT_ID, stock="0050" , date_from='2020-01-01' ):
  """
  進行個股K線繪製，回傳至於雲端圖床的連結。將顯示包含5MA、20MA及量價關係，預設為'2020-01-01'迄今收盤價。
  :stock :個股代碼(字串)，預設0050。
  :date_from :起始日(字串)，格式為%Y-%m-%d，預設自2020-01-01起。
  """
  stock = str(stock)+".tw"
  df = web.DataReader(stock, 'yahoo', date_from) 
  mpf.plot(df,type='candle',mav=(5,20),volume=True,title=stock.upper() ,savefig='testsave.png')
  PATH = "testsave.png"
  im = pyimgur.Imgur(CLIENT_ID)
  uploaded_image = im.upload_image(PATH, title=stock+" candlestick chart")
  return uploaded_image.link

  result = plot_stcok_k_chart(CLIENT_ID,"0050","2020-09-01")
print(result)

from IPython.display import Image
from IPython.core.display import HTML 
Image(result) 