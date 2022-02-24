import Vue from 'vue'
import VueRouter from 'vue-router'
import Dashboard from '../components/Dashboard.vue'
import LoanList from '../components/LoanList.vue'
import NewLoan from '../components/NewLoan.vue'
import NewClient from '../components/NewClient.vue'
import CreateExpense from '../components/CreateExpense.vue'
import Client from '../views/Client.vue'
import Login from '../views/Login.vue'
import CashFlowStatement from '../components/CashFlowStatement.vue'
import Home from '../views/Home.vue'
import store from "@/store"

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/clients',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/createClient',
    name: 'CreateClient',
    component: NewClient,
    meta: { requiresAuth: true }
  },  
  {
    path: '/loans/pending',
    name: 'PendingLoans',
    component: LoanList,
    props: {
      loan_status: 'pending'
    },
    meta: { requiresAuth: true }
  },
  {
    path: '/loans/approved',
    name: 'ApprovedLoans',
    component: LoanList,
    props: {
      loan_status: 'approved'
    },
    meta: { requiresAuth: true }
  },
  {
    path: '/loans/declined',
    name: 'DeclinedLoans',
    component: LoanList,
    props: {
      loan_status: 'declined'
    },
    meta: { requiresAuth: true }
  },
  {
    path: '/createLoan',
    name: 'createLoan',
    component: NewLoan,
    meta: { requiresAuth: true }
  },
  {
    path: '/client/:id',
    name: 'ClientDetail',
    component: Client,
    meta: { requiresAuth: true }
  },
  {
    path: '/cashFlowStatement',
    name: 'CashFlowStatement',
    component: CashFlowStatement,
    props: {
      initialType: 'daily'
    },
    meta: { requiresAuth: true }
  },
  {
    path: '/rangedCashFlowStatement',
    name: 'RangedCashFlowStatement',
    component: CashFlowStatement,
    props: {
      initialType: 'ranged'
    },
    meta: { requiresAuth: true }
  },
  {
    path: '/createExpense',
    name: 'CreateExpense',
    component: CreateExpense,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { guest: true }
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, _, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (store.getters.isAuthenticated) {
      next();
      return;
    }
    next("/login");
  } else {
    next();
  }
});

router.beforeEach((to, _, next) => {
  if (to.matched.some((record) => record.meta.guest)) {
    if (store.getters.isAuthenticated) {
      next("/");
      return;
    }
    next();
  } else {
    next();
  }
});

export default router
