import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false

import axios from 'axios';
import VueAxios from 'vue-axios';
import Qs from "qs";
import router from './router'


var axios_instance = axios.create({
    transformRequest: [function (data) {
        data = Qs.stringify(data);
        return data;
    }],
    timeout: 40000,
    headers: {'Content-Type': 'application/x-www-form-urlencoded' , 'Pragma': 'no-cache' , 'cache-control' : 'no-cache' },
    // responseType: 'json'
});


axios_instance.interceptors.response.use(
    (response) => {
        try {
            if (response.data !== null && typeof response.data === 'object' ) {
                let data = response.data;
                let reUrl = response.request.responseURL;
                if (data.status === 500 ){
                    var errorMsg = "";
                    var errorCode = null;
                    if (data.errorState === "self_error" ){
                        errorCode = 111;
                        errorMsg = "SYSTEM.ERROR";
                    }
                    if (data.errorState === "logic" ){
                        let msg = this.$geti18(data.msg);
                        errorMsg = msg? data.msg : "SYSTEM.ERROR";
                    }
                    if (data.errorState === "dsr_error" ){
                        let testgex = /^D-\d{3}-\d+$/;
                        console.log(this.$te);
                        let isExist = this.$te(data.msg);
                        if (isExist) {
                            let msg = this.$geti18(data.msg);
                            errorMsg = msg;
                        }else if ( testgex.test(data.errCode) && this.$geti18(data.errCode)  ) {
                            let errCodeFullExist = this.$te("DSR.RejCode." + data.errCode.split("-")[2] );
                            if (errCodeFullExist){
                                errorMsg = this.$geti18( "DSR.RejCode." + data.errCode.split("-")[2] );
                            }else{
                                errorMsg =  "SYSTEM.ERROR";
                            }
                        }else{
                            errorMsg =  "SYSTEM.ERROR";
                        }
                    }
                    let Err = new Error(data.status);
                    Err.code = errorCode || data.errCode;
                    Err.data = data;
                    Err.msg = errorMsg || data.msg;
                    throw Err;
                }else if ( data.status === 404 ){
                    let Err = new Error(data.status);
                    Err.code = data.errCode;
                    Err.data = data;
                    Err.msg = "SYSTEM.ERROR";
                    throw Err;
                }else{
                    return data.data;
                }
            }else{
                let Err = new Error('Non-JSON Respond');
                Err.code = 515; Err.response = response;
                throw Err;
            }
        } catch (err) {
            // Vue.prototype.$EventHubs.$emit('responseError', response);
            return Promise.reject(err);
        }
    },
    (e) => {
        if (e.code === "ECONNABORTED") {
            //TODO
            e.code = 2014;
            e.msg = "op.timeout";
            return Promise.reject(e);
        }
        e.response = {};
        if ( process.env.NODE_ENV === "production" && e =="Cancel" && !!( e.constructor && e.constructor.call && e.constructor.apply)  ){
            e.code = 514;
            return Promise.reject(e);
        }else if ( e.constructor.name === "Cancel" ){
            e.code = 514;
            return Promise.reject(e);
        }
        Vue.config.errorHandler.call( null , e , this, e.request ) ;
        // Vue.prototype.$EventHubs.$emit('responseError', e);
        return Promise.reject(e);
        // return Promise.reject(error.response.data)   // 返回接口返回的错误信息
    });

Vue.use(VueAxios, axios_instance, axios);
// #119->userId
// #114416 , 3400 , 17750 ,83601 => 0.7
// # 127020.0 => 0.3
// # 127579.0 => 0.3

//114416->相機
//119,7488->ram 17750
//127579 -> 三國
Vue.prototype.$userId = 114416;

new Vue({
    vuetify,
    router,
    render: h => h(App)
}).$mount('#app')
