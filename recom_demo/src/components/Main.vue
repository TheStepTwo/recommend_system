<template>
  <v-app id="inspire">
    <v-card

    >
      <v-toolbar
              color="indigo darken-2"
              dark
      >
        <v-app-bar-nav-icon ></v-app-bar-nav-icon>

        <v-toolbar-title>CISC7201 INTRODUCTION TO DATA SCIENCE PROGRAMMING</v-toolbar-title>

        <v-spacer></v-spacer>

        <v-btn icon>
          <v-icon>mdi-dots-vertical</v-icon>
        </v-btn>
      </v-toolbar>

      <v-card-text>

        <div style="width: 70%;margin: 0 auto">
          <v-text-field
                  v-model="keyword"
                  background-color="white"
                  color="blue darken-2"
                  solo
                  label="Searching..."
                  single-line
                  prepend-inner-icon="mdi-magnify"
                  v-on:keyup.enter="searchKeywords"
          ></v-text-field>
          <div class="hot-tag-div">
            <span class="top-tag-title" style=";color:black" >Hot : </span>
            <span v-for="hotItem in hotItems" class="top-tag-item"><a v-on:click="onClickHotItem(hotItem)" >{{ hotItem.cut_name  }}</a></span>
          </div>
        </div>

      </v-card-text>
      <br>


    </v-card>

    <v-card v-if="searchedItems.length > 0" style="background-color: #e9ebee">
      <v-card-text>

        <div style="width: 60%;margin: 0 auto;">
          <div style="font-size: 15px;color:black">
            Search Result:
          </div>

          <v-list two-line>
            <v-list-item-group
                    active-class="pink--text"
            >
              <template v-for="(item, index) in searchedItems">
                <v-list-item :key="item.title" v-on:click="onClickSearchedItem(item)" >
                  <template v-slot:default="{ active, toggle }">
                    <v-list-item-content>
                      <v-list-item-title v-text="item.product_name"></v-list-item-title>
                      <div>
                        <div  style="margin-top:10px;" >
                          <v-chip small class="ma-2 main-cat" style="margin-left:0 !important;"  label  >{{ item.cat1_name }}</v-chip>
                          <v-chip small class="ma-2 main-cat" style="margin-left:0 !important;"  label  >{{ item.cat2_name }}</v-chip>
                          <v-chip small class="ma-2 main-cat" style="margin-left:0 !important;"  label  >{{ item.cat3_name }}</v-chip>
                        </div>
                        <v-slider
                                style="color: red"
                                small
                                readonly
                                :value="item.cos"
                                color="blue darken-4"
                                min="0"
                                :max="10000"
                                label="Similarity"
                        ></v-slider>
                      </div>
                      <!--<v-list-item-subtitle v-text="item.productId"></v-list-item-subtitle>-->
                    </v-list-item-content>
                  </template>
                </v-list-item>

                <v-divider
                        :key="index"
                ></v-divider>
              </template>
            </v-list-item-group>
          </v-list>

        </div>

      </v-card-text>

    </v-card  >

    <v-card v-else  style="background-color: #f9f9f9">
      <v-card-text>

        <div style="width: 60%;margin: 0 auto;">
          <div style="font-size: 15px;color:black;margin-left:17px;">
            Recommend for you
          </div>

          <v-list two-line>
            <v-list-item-group
                    active-class="pink--text"
            >
              <template v-for="(item, index) in userCfItems">
                <v-list-item :key="item.title" v-on:click="onClickSearchedItem(item)" >
                  <template v-slot:default="{ active, toggle }">
                    <v-list-item-content>
                      <v-list-item-title v-text="item.product_name"></v-list-item-title>
                      <div  style="margin-top:10px;" >
                        <v-chip small  class="ma-2" style="margin-left:0 !important;" label  >{{ item.cat1_name }}</v-chip>
                        <v-chip small class="ma-2"  style="margin-left:0 !important;" label  >{{ item.cat2_name }}</v-chip>
                        <v-chip small class="ma-2" style="margin-left:0 !important;" label  >{{ item.cat3_name }}</v-chip>
                      </div>
                      <!--<v-list-item-subtitle v-text="item.productId"></v-list-item-subtitle>-->
                    </v-list-item-content>
                  </template>
                </v-list-item>

                <v-divider></v-divider>
              </template>
            </v-list-item-group>
          </v-list>

        </div>
      </v-card-text>
    </v-card>


    <v-dialog
            v-model="isLoading"
            hide-overlay
            persistent
            width="300"
    >
      <v-card
              color="primary"
              dark
      >
        <v-card-text>
          Loading...
          <v-progress-linear
                  indeterminate
                  color="white"
                  class="mb-0"
          ></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!--<div class="v-card v-card&#45;&#45;flat v-sheet v-sheet&#45;&#45;tile theme&#45;&#45;light grey lighten-4" style="height: 200px;"><header class="v-sheet v-sheet&#45;&#45;tile theme&#45;&#45;light v-toolbar v-toolbar&#45;&#45;extended blue darken-3" style="height: 164px;"><div class="v-toolbar__content" style="height: 64px;"><button type="button" class="v-app-bar__nav-icon v-btn v-btn&#45;&#45;flat v-btn&#45;&#45;icon v-btn&#45;&#45;round theme&#45;&#45;light v-size&#45;&#45;default"><span class="v-btn__content"><i aria-hidden="true" class="v-icon notranslate mdi mdi-menu theme&#45;&#45;light"></i></span></button><div class="v-toolbar__title">Title</div><div class="spacer"></div><button type="button" class="v-btn v-btn&#45;&#45;flat v-btn&#45;&#45;icon v-btn&#45;&#45;round theme&#45;&#45;light v-size&#45;&#45;default"><span class="v-btn__content"><i aria-hidden="true" class="v-icon notranslate mdi mdi-magnify theme&#45;&#45;light"></i></span></button><button type="button" class="v-btn v-btn&#45;&#45;flat v-btn&#45;&#45;icon v-btn&#45;&#45;round theme&#45;&#45;light v-size&#45;&#45;default"><span class="v-btn__content"><i aria-hidden="true" class="v-icon notranslate mdi mdi-heart theme&#45;&#45;light"></i></span></button><button type="button" class="v-btn v-btn&#45;&#45;flat v-btn&#45;&#45;icon v-btn&#45;&#45;round theme&#45;&#45;light v-size&#45;&#45;default"><span class="v-btn__content"><i aria-hidden="true" class="v-icon notranslate mdi mdi-dots-vertical theme&#45;&#45;light"></i></span></button><br><div style="clear: both;width: 100%;display: block;">df</div></div><div class="v-toolbar__extension" style="height: 100px;"></div></header></div>-->
  </v-app>
</template>

<script>
    import {Api} from '../service/ApiService';
    import router from '../router/index'
    export default {
        name: "Main",
        mixins: [Api],
        props: {
            source: String,
        },
        data: () => ({
            hotItems: [],
            isLoading: false,
            keyword : '',
            searchedItems: [],
            userCfItems: [],
        }),
        methods: {
            goProduct(productId){
                router.push({ name : 'Product' , params : { 'productId' :  productId } , query : {} });
            },
            searchKeywords() {
                console.log(this.keyword);
                if (!this.keyword.trim()) return;
                this.isLoading = true;
                this._getSearch({
                    query_str : this.keyword
                }).then((res) => {
                    this.isLoading = false;
                    res.forEach((e)=>{
                        e.cos = parseInt(e.cos*10000)
                    });

                    this.searchedItems = res;
                }).catch((e) => {
                    console.error(e);
                    this.isLoading = false;
                });
            },
            onClickSearchedItem(item){
                console.log(item);
                this.goProduct(item.productId);
            },
            onClickHotItem(hotItem){
                this.keyword = hotItem.cut_name;
                this.searchKeywords();
            },
            findRecommentForUserCf(){
                this.isLoading = true;
                //7488
                this._getRecommendUserCf({
                    userid : this.$userId
                }).then((res) => {
                    console.log(res);
                    this.isLoading = false;
                    this.userCfItems = res;
                }).catch((e) => {
                    console.error(e);
                    this.isLoading = false;
                });
            }

        },
        mounted() {
            console.log(Api);
            this.isLoading = true;
            this._getTopNWord()
                .then((res) => {
                    console.log(res);
                    res = res.slice(0, 12);
                    this.hotItems = res;
                    this.isLoading = false;
                }).catch((e) => {
                  console.error(e);
                  this.isLoading = false;
                  alert("Loading data wrong!")
            });
            this.findRecommentForUserCf();
//
//            this._getSearch({
//                query_str : 'python'
//            }).then((res) => {
//                console.log(res);
//            }).catch((e) => {
//                console.error(e);
//                alert('獲取業務類型錯誤!' + e.toString())
//            });
//
//            //7488
//            this._getRecommendUserCf({
//                userid : 114416
//            }).then((res) => {
//                console.log(res);
//            }).catch((e) => {
//                console.error(e);
//                alert('獲取業務類型錯誤!' + e.toString())
//            });
//
//            this._getRecommendItemCf({
//                itemid : '489000'
//            }).then((res) => {
//                console.log(res);
//            }).catch((e) => {
//                console.error(e);
//                alert('獲取業務類型錯誤!' + e.toString())
//            });


        }
    }
</script>