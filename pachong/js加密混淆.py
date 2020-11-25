'''
    教程博客地址https://www.cnblogs.com/bobo-zhang/p/11243138.html
    - 分析：https://www.aqistudy.cn/html/city_detail.html
        - 1、当我们更改了页面的查询条件后，点击查询按钮，在浏览器抓包工具中会捕获到两个一样的数据包，
            我们只要能破解其中的一个数据包的内容，剩下的一个也可以破解
            - 请求的url：https://www.aqistudy.cn/apinew/aqistudyapi.php
            - 请求方式：post
            - 请求参数：d：一组动态变化的加密数据值
            - 返回的响应数据就是我们想要的捕获的指标数据
                - 响应数据也被加密，是一组被加密的密文数据，我们必须将密文数据解密成原文数据后才能被我们使用

        - 2、我们在点击查询按钮后，发现页面没有全局刷新，则表示点击查询后发起的请求是ajax请求。
            - 发起的ajax请求对应的数据包就是我们在步骤1表示的数据包
            - 该aja请求发送的时候请求的：
                - 请求url：https://www.aqistudy.cn/apinew/aqistudyapi.php
                - 请求方式：post
                - 请求参数：d：一组动态变化的加密数据值
                - 响应数据也被加密
            - 请求回来的数据是一组密文数据，但是在前台展示的数据是明文数据
                说明前台把密文数据进行解密了
                    - 前台存在解密方案，我们需要将其解密方案获取到，就可以对其密文进行解密了
                    - 其解密方案肯定存在于页面请求的某个文件中
        - 3、点击查询按钮发起的是ajax请求，ajax的请求一定是用js写的，在ajax请求的代码中，可以看到那些具体的操作
            - 请求的url
            - 请求的方式
            - 携带的请求参数
                - 可以从ajax的代码中获取
                - 为什么请求参数不可以从抓包工具中获取？
                    - 因为请求参数是动态加密的数据
            - 请求回来的数据对应的回调函数
                - 解密方案就在回调函数中，回调函数的参数就是请求到的响应数据（加密的密文数据），
                  该函数会对拿到的密文数据进行解密，解密后的原文动态显示在前台页面中
                - 重点：只要能找到点击查询的按钮对应的ajax请求代码后，就可以知道动态变化且加密的请求参数如何生成，
                       然后我们就可以使用该方式动态生成一组请求参数，然后基于指定的url进行请求发送，获取加密的响应数据，
                       获取的密文数据就可以通过ajax请求代码中国的回调函数操作中获取解密方案，使用该方案对加密的响应数据进行解密
            - 操作：找到查询按钮对应的ajax请求打码
                - 方案： 获取搜索按钮对应的点击时间绑定的函数
                    - 最好使用【火狐浏览器】寻找点击时间的函数代码
                    - 使用火狐浏览器找到【查询】按钮对应的元素，找到event事件
                        function getData()
                           {
                              state = 0;
                                  city=$('#city').val();
                                  $.cookie('dcity', city, {expires : 30});
                                  //type = $('#type').combobox('getValue');
                                  type = $('input:radio[name=type]:checked').val();
                                  getTimeSel();

                                  if(type=="HOUR")
                                  {
                                     var timediff = converTimeFormat($('#dtbEndTime').datetimebox('getValue')).getTime()-converTimeFormat($('#dtbStartTime').datetimebox('getValue')).getTime();
                                     if(timediff >30*24*3600*1000)
                                     {
                                        showMessage(false,"按小时查询仅支持查询一个月数据，查看长时间变化趋势请选择按日查询！");
                                        return ;
                                     }
                                  }
                                  getAQIData();
                                  getWeatherData();
                           }
                    - 函数内没有ajax代码，那么可能存在于getAQIData();getWeatherData();这两个函数中
                        if(type=="HOUR") 表示是以小时为单位进行查询的
                    - 进入getAQIData();getWeatherData();内部找寻ajax代码
                        在这两个函数内部都调用了getServerData(）函数，ajax存在于getServerData（）这个函数中
                        但是，这两个函数中并没有ajax请求
                        那么我们就去network里进行全局搜索getServerData
                            在jQuery代码里找到了getServerData函数
                                局部搜索getServerData
                                    - 找到的结果看上去像是密文
                                    - js混淆：
                                        - 在网站后台，关键的重要的js函数的实现为了保密，一般会对这些js函数代码进行混淆（理解成加密），讲加密的js函数进行解密
                                    - js反混淆： 反混淆转换网站https://www.jisuan.mobi/p6Hm3bB1Bbm66xiS.html
                                        在转换后的js函数里搜索getServerData找到getServerData函数
                                            function getServerData(method, object, callback, period) {
                                                 const key = hex_md5(method + JSON.stringify(object));
                                                 const data = getDataFromLocalStorage(key, period);
                                                 if (!data) {
                                                  var param = getParam(method, object);
                                                  $.ajax({
                                                   url: '../apinew/aqistudyapi.php',
                                                   data: {
                                                    d: param
                                                   },
                                                   type: "post",
                                                   success: function(data) {
                                                    data = decodeData(data);
                                                    obj = JSON.parse(data);
                                                    if (obj.success) {
                                                     if (period > 0) {
                                                      obj.result.time = new Date().getTime();
                                                      localStorageUtil.save(key, obj.result)
                                                     }
                                                     callback(obj.result)
                                                    } else {
                                                     console.log(obj.errcode, obj.errmsg)
                                                    }
                                                   }
                                                  })
                                                 } else {
                                                  callback(data)
                                                 }
                                                }
                        - decodeData(data)将加密的数据进行解密
                        - getParam(method, object)可一获取加密变化的请求参数
                    - 上面的两个函数是js函数，我们写的爬虫程序是Python，Python如何调用js函数？
                        - Python如何调用js函数
                            - 方式1：
                                - 将js函数改写成Python函数
                            - 方式2：
                                - 使用相关模块记进行js逆向
                        - js逆向：
                            - 将js函数改写成Python函数
                            - Python使用PyExecJS这个模块，是一个可以用Python来模拟运行JavaScript的库
                                还需要安装node js的开发环境
                            - 把找到的所有的js代码保存在一个文件里
                                并自己自定义一个调用getParam的函数，因为我需要自己传递自定义参数对其进行参数的封装，
                                1、最终把自定义参数传到getParam函数里面
                                    function getPostParamcode(method, city,type, startTime, endTime){
                                        var param = {}
                                        param.city = city;
                                        param.type = type;
                                        param.startTime = startTime;
                                        param.endTime = endTime;
                                        return getParam(method, param)
                                    }
                                2、模拟执行js源文件中的js函数
                                    - 使用Python使用PyExecJS这个模块，去调用getPostParamcode并传入参数，返回一个加密的请求参数
                                    - 使用requests模块对其进行请求，返回加密的动态数据
                                3、对其加密的返回的数据进行解密
                                    - 模拟执行decodeData（）进行数据解密



'''
#使用模块进行js逆向，模拟调用js源文件中的getParam函数