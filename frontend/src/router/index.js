import Vue from 'vue'
import VueRouter from 'vue-router'
import Dashboard from '../components/Dashboard.vue'
import LoanList from '../components/LoanList.vue'
import NewLoan from '../components/NewLoan.vue'
import NewClient from '../components/NewClient.vue'
import Client from '../views/Client.vue'
import CashFlowStatement from '../components/CashFlowStatement.vue'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/clients',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/createClient',
    name: 'CreateClient',
    component: NewClient,
  },  
  {
    path: '/loans/pending',
    name: 'PendingLoans',
    component: LoanList,
    props: {
      loan_status: 'pending'
    }
  },
  {
    path: '/loans/approved',
    name: 'ApprovedLoans',
    component: LoanList,
    props: {
      loan_status: 'approved'
    }
  },
  {
    path: '/loans/declined',
    name: 'DeclinedLoans',
    component: LoanList,
    props: {
      loan_status: 'declined'
    }
  },
  {
    path: '/createLoan',
    name: 'createLoan',
    component: NewLoan
  },
  {
    path: '/client/:id',
    name: 'ClientDetail',
    component: Client
  },
  {
    path: '/cashFlowStatement',
    name: 'CashFlowStatement',
    component: CashFlowStatement,
    props: {
      initialType: 'daily'
    }
  },
  {
    path: '/rangedCashFlowStatement',
    name: 'RangedCashFlowStatement',
    component: CashFlowStatement,
    props: {
      initialType: 'ranged'
    }
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
