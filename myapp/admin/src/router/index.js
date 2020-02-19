import Vue from "vue";
import VueRouter from "vue-router";

import Home from "../views/Home.vue";
import Login from "../views/Login.vue";

import ArticleList from "../views/ArticleList.vue";
import ArticleEdit from "../views/ArticleEdit.vue";

import AdminUserList from "../views/AdminUserList.vue";
import AdminUserEdit from "../views/AdminUserEdit.vue";

Vue.use(VueRouter);

const routes = [
  { path: "/login", name: "login", component: Login, meta: { isPublic: true } },

  {
    path: "/",
    name: "home",
    component: Home,
    redirect: "/articles/index",
    children: [
      {
        path: "/articles/create",
        component: ArticleEdit
      },
      {
        path: "/articles/index",
        component: ArticleList
      },
      {
        path: "/articles/edit/:id",
        component: ArticleEdit,
        props: true
      },
      { path: "/admin_users/create", component: AdminUserEdit },
      { path: "/admin_users/edit/:id", component: AdminUserEdit, props: true },
      { path: "/admin_users/list", component: AdminUserList }
    ]
  }
];

const router = new VueRouter({
  routes
});

//全局前置守卫
router.beforeEach((to, from, next) => {
  if (!to.meta.isPublic && !localStorage.token) {
    Vue.prototype.$message({
      type: "error",
      message: "请先登录" 
    });
    return next("/login");
  }
  next();
});

export default router;
