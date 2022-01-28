<template>
  <div class="home">
    <!-- <div class="container is-fluid">
      <div class="columns" id="canvas">
        <div class="column is-narrow">
            <b-menu class="has-text-left" style="width: 300px;">
              <b-menu-list>
                <b-menu-item icon="users" label="Clients" @click="selectedView='dashboard'"></b-menu-item>
                <b-menu-item icon="university" :active="false">
                  <template #label="props">
                    Loans
                    <b-icon class="is-pulled-right" :icon="props.expanded ? 'caret-up' : 'caret-down'"></b-icon>
                  </template>
                  <b-menu-item label="Create New Loan" @click="selectedView='newloan'"></b-menu-item>
                  <b-menu-item label="Pending" @click="selectedView='pendingloans'"></b-menu-item>
                  <b-menu-item label="Approved" @click="selectedView='approvedloans'"></b-menu-item>
                  <b-menu-item label="Declined" @click="selectedView='declinedloans'"></b-menu-item>
                </b-menu-item>
                <b-menu-item icon="money-check" label="Create Collection Record" @click="selectedView='createcollection'"></b-menu-item>
                <b-menu-item icon="money-bill-wave" label="Create CA" @click="selectedView='createca'"></b-menu-item>
                <b-menu-item icon="user-plus" label="New Client" @click="selectedView='newclient'"></b-menu-item>
                <b-menu-item icon="print" :active="false">
                  <template #label="props">
                    Reports
                    <b-icon class="is-pulled-right" :icon="props.expanded ? 'caret-up' : 'caret-down'"></b-icon>
                  </template>
                  <b-menu-item label="Daily General Report"></b-menu-item>
                  <b-menu-item label="Daily Collection"></b-menu-item>
                  <b-menu-item label="Daily Transaction"></b-menu-item>
                </b-menu-item>
              </b-menu-list>
            </b-menu>
        </div>
        <div class="column">
          <div class="box" v-if="selectedView == 'dashboard'">
            <Dashboard/>
          </div>
          <div class="box" v-else-if="selectedView == 'newclient'">
            <NewClient/>
          </div>
          <div class="box" v-else-if="selectedView == 'newloan'">
            <NewLoan/>
          </div>
          <div class="box" v-else-if="selectedView == 'pendingloans'">
            <LoanList loan_status="pending"/>
          </div>
          <div class="box" v-else-if="selectedView == 'approvedloans'">
            <LoanList loan_status="approved"/>
          </div>
          <div class="box" v-else-if="selectedView == 'declinedloans'">
            <LoanList loan_status="declined"/>
          </div>
        </div>
      </div>
    </div> -->
  </div>
</template>

<script>
// @ is an alias to /src
import Dashboard from '@/components/Dashboard.vue'
import NewClient from '@/components/NewClient.vue'
import NewLoan from '@/components/NewLoan.vue'
import LoanList from '@/components/LoanList.vue'

export default {
  name: 'Home',
  filters: {
    longDate (date) {
      return date.toDateString();
    }
  },
  data() {
    return {
      today: new Date(),
      selectedView: 'dashboard'
    }
  },
  components: {
    Dashboard,
    NewClient,
    NewLoan,
    LoanList
  }
}
</script>

<style>
 .home {
   margin-top: 1em;
   font-size: 21px;
 }

 #canvas {
   margin-top: 1.5em;
 }
</style>