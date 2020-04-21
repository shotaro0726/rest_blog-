<template>
   <main class="container">
        <p id="lead">{{postCount}}件中 {{postRangeFirst}}~{{postRangeLast}}件を一覧表示</p>
        <section>
            <router-link :to="{name: 'detail', params: {id: post.id}}" v-for="post of postList" :key="post.id"
                         class="post">
                <article>
                    <figure>
                        <img :src="post.thumbnail" :alt="post.title" class="thumbnail">
                    </figure>
                    <div class="post-main" v-html="post.main_text"></div>
                    <p class="post-category" :style="{'color': post.category.color}">{{post.category.name}}</p>
                    <h2 class="post-title">{{post.title}}</h2>
                    <p class="post-lead">{{post.lead_text}}</p>
                </article>
            </router-link>
        </section>
        <hr class="divider">
        <nav id="page">
            <nav id="back"><a @click="goBack" title="前ページへ戻る"><img src="@/assets/back.png"></a></nav>
            <span>Page {{postCurrentPageNumber}}</span>
            <router-link v-if="hasNext" :to="getPostNextURL" id="next"><img src="@/assets/next.png"></router-link>
        </nav>
    </main>
</template>

<script>
    import {mapGetters, mapActions} from 'vuex'
    import {UPDATE_POSTS} from "@/store/mutation-types";

    export default {
        name: 'post-list',
        data() {
            return {
                post: null,
                hasBefore: false,
            }
        },
        beforeRouteEnter(to, from, next){
            next(component => {
                if(from.name){
                    component.hasBefore = true
                }
            })
        },
        watch: {
            '$route'() {
                this.getPosts()
            }
        },
        created() {
            this.getPosts()
        },
        computed: {
            ...mapGetters([
                'postList', 'postCount', 'postRangeFirst', 'postRangeLast',
                'postCurrentPageNumber', 'hasPrevious', 'hasNext', 'getPreviousURL', 'getNextURL'
            ]),
            getPostPreviousURL() {
                const url = new URL(this.getPreviousURL)
                const keyword = url.searchParams.get('keyword') || ''
                const category = url.searchParams.get('category') || ''
                const page = url.searchParams.get('page') || 1
                return this.$router.resolve({
                    name: 'posts',
                    query: {keyword, category, page}
                }).route.fullPath
            },
            getPostNextURL() {
                const url = new URL(this.getNextURL)
                const keyword = url.searchParams.get('keyword') || ''
                const category = url.searchParams.get('category') || ''
                const page = url.searchParams.get('page')
                return this.$router.resolve({
                    name: 'posts',
                    query: {keyword, category, page}
                }).route.fullPath
            }
        },
        methods: {
            ...mapActions([UPDATE_POSTS]),
            getPosts() {
                let postURL = this.$httpPosts
                const params = this.$route.query
                const queryString = Object.keys(params).map(key => key + '=' + params[key]).join('&')
                if (queryString) {
                    postURL += '?' + queryString
                }
                this.$http(postURL)
                    .then(response => {
                        return response.json()
                    })
                    .then(data => {
                        this[UPDATE_POSTS](data)
                    })
            },
            goback() {
                if(this.hasBefore) {
                    this.$router.go(-1)
                }else{
                    this.$router.push({name:'posts'})
                }
            },
        }
    }
</script>

<style scoped>
    #back {
        margin-bottom: 80px;
    }
    #back a {
        cursor: pointer;
        width: 44px;
        display: inline-block;
    }
    #top a {
        cursor: pointer;
        color: #999;
        display: inline-block;
        width: 44px;
    }
    .post-category{
        font-size: 12px;
    }
    .post-title{
        font-weight: bold;
        font-size: 14px;
    }
    .post-lead{
        margin-top: 10px;
    }
    .divider{
        margin-top: 80px;
        margin-bottom: 80px;
        width: 100%;
        height: 0;
        border: solid 1px #ccc;
    }
    .post-main{
        width: 100%;
        line-height: 2;
    }
    .post-main p{
        margin-bottom: 4em;
    }
    .post-main img{
        max-width: 100%;
        height: auto;
        box-shadow: 0 0 5px #ccc;
    }
    @media(min-width: 768px){
        .post-title{
            width: 440px;
        }
        .post-lead{
            width: 440px;
        }
        .divider{
            width: 650px;
        }
        .post-main{
            width: 650px;
        }
    }
</style>