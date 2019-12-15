import Vue from 'vue'
import Router from 'vue-router'
import Main from '../components/Main.vue'
import Product from '../components/Product.vue'

Vue.use(Router);

const router =  new Router({
    routes: [
    {
        path: '/',
        name : 'Main',
        component: Main,
    },
    {
        path: '/product/:productId',
        name : 'Product',
        component: Product,
    },
  ],
  // scrollBehavior(to, from , savedPosition){
  //   if ( ! to.meta.keepAlive ){
  //       window.scrollTo(0,0);
  //   }else{
  //     return savedPosition || { x: 0 , y : 0 };
  //   }
  // }
});
// router.replace({ path: '/' , redirect: '/searchEmployee' });
export default router;
