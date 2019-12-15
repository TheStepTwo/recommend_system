<template>
  <v-app id="inspire">

    <v-card style="background-color: #e9ebee"
    >
      <v-toolbar
              color="indigo darken-2"
              dark
      >
        <v-app-bar-nav-icon ></v-app-bar-nav-icon>

        <v-toolbar-title>CISC7201 INTRODUCTION TO DATA SCIENCE PROGRAMMING</v-toolbar-title>

        <v-spacer></v-spacer>

        <v-scale-transition>
          <v-btn
                  key="export"
                  icon
          >
            <v-icon>mdi-export-variant</v-icon>
          </v-btn>
        </v-scale-transition>
        <v-scale-transition>
          <v-btn
                  key="delete"
                  icon
          >
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-scale-transition>

        <v-btn icon>
          <v-icon>mdi-dots-vertical</v-icon>
        </v-btn>
      </v-toolbar>


      <v-row no-gutters>
        <v-col
                cols="8"
        >
          <v-card
                  class="pa-2"
                  outlined
                  tile
          >
            <v-card-text v-if="product" style="width: 600px">

              <div style="padding: 20px"  >
                <div class="product-title" >{{ product.product_name }}</div>
                <div style="margin-top: 10px;">
                  <v-chip class="ma-2" color="primary" >{{ product.cat1_name }}</v-chip>
                  <v-chip class="ma-2" color="secondary">{{ product.cat2_name }}</v-chip>
                  <v-chip class="ma-2" color="red" text-color="white">{{ product.cat3_name }}</v-chip>
                </div>

                <div class="mt-5">
                  <span style="color: black" >Avg. Rating:</span>
                  <v-rating
                          readonly
                          v-model="product.rating"
                          color="yellow darken-3"
                          background-color="grey darken-1"
                          empty-icon="$ratingFull"
                          half-increments
                          hover
                  ></v-rating>
                </div>
              </div>

            </v-card-text>

          </v-card>
        </v-col>
        <v-col
                cols="4"
        >
          <v-card
                  class="pa-2"
                  outlined
                  tile
          >
            <v-list-item>
              <template v-slot:default="{ active }">
                <v-list-item-content>
                  <v-list-item-title>Guess You also Like...</v-list-item-title>
                </v-list-item-content>
              </template>
            </v-list-item>
            <template v-for="item in recommendItem" style="width:400px;" >
            <v-list-item>
            <template v-slot:default="{ active }">
              <v-list-item-content>
                <v-list-item-title>{{ item.product_name }}</v-list-item-title>
                <v-list-item-subtitle>{{ item.cat1_name }} | {{ item.cat2_name }} | {{ item.cat3_name }}</v-list-item-subtitle>
              </v-list-item-content>
              </template>
              </v-list-item>
              <v-divider></v-divider>
            </template>
          </v-card>
        </v-col>
      </v-row>



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


  </v-app>
</template>

<script>
    import {Api} from '../service/ApiService';
    export default {
        mixins: [Api],
        name: "Product",
        props: {
            source: String,
        },
        data: () => ({
            isLoading: false,
            product: null,
            recommendItem: []
        }),
        methods: {
            getProduct(){
              this.isLoading = true;
              //7488
              this._getProductByProductId({
                  productId : this.$route.params.productId
              }).then((res) => {
                  this.isLoading = false;
                  this.product = res;
              }).catch((e) => {
                  console.error(e);
                  this.isLoading = false;
              });
            },
            getRecommendItemCf(){
                this.isLoading = true;
                //7488
                this._getRecommendItemCf({
                    itemid : this.$route.params.productId
                }).then((res) => {
                    console.log(res);
                    this.isLoading = false;
                    this.recommendItem = res;
                }).catch((e) => {
                    console.error(e);
                    this.isLoading = false;
                });
            },
        },
        mounted() {
            this.isLoading = true;
            this._getProductByProductId({
                productId : this.$route.params.productId
            }).then((res) => {
                this.product = res;
                return this._getRecommendItemCf({
                    k: 15,
                    itemid : this.$route.params.productId
                });
            }).then((res) => {
                this.recommendItem = res;
                this.isLoading = false;
            }).catch((e) => {
                console.error(e);
                this.isLoading = false;
            });
        }
    }
</script>