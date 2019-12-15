export const  Api =  {
    data() {
      return {
        prod: process.env.NODE_ENV === "production",
        apiUrl: 'http://127.0.0.1:5000/'
      }
    },
    methods: {
        _getTopNWord(){
            return this.$http.get( this.apiUrl + "top_n");
        },
        _getSearch(data){
            return this.$http.get( this.apiUrl + "search" , { params: data } )
        },
        _getRecommendItemCf(data){
            return this.$http.get( this.apiUrl + "recommend_item_cf" , { params: data } )
        },
        _getRecommendUserCf(data){
            return this.$http.get( this.apiUrl + "recommend_user_cf" , { params : data } )
        },
        _getProductByProductId(data){
            return this.$http.get( this.apiUrl + "find_product" , { params : data } )
        },

    }
}
