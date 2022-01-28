<template>
  <div id="app">
    <b-navbar>
        <template #brand>
            <b-navbar-item tag="router-link" :to="{ path: '/' }">
              <a href="/">
                <h1 class="is-size-5">
                  ION
                  <strong class="is-size-7">Loan Application</strong>
                </h1>
              </a>
            </b-navbar-item>
        </template>

        <!-- <template #end>
            <b-navbar-item tag="div">
                <div class="buttons">
                    <a class="button is-primary">
                        <strong>Sign up</strong>
                    </a>
                    <a class="button is-light">
                        Log in
                    </a>
                </div>
            </b-navbar-item>
        </template> -->
    </b-navbar>

    <div class="container is-fluid" id="canvas">
      <!-- <h1>Hello! Today is {{ today | longDate }}</h1> -->
      <div class="columns">
        <div class="column is-narrow">
            <b-menu class="has-text-left" style="width: 300px;" :activable="false">
              <b-menu-list>
                <b-menu-item icon="users" label="Clients" tag="router-link" to="/"></b-menu-item>
                <b-menu-item icon="university">
                  <template #label="props">
                    Loans
                    <b-icon class="is-pulled-right" :icon="props.expanded ? 'caret-up' : 'caret-down'"></b-icon>
                  </template>
                  <b-menu-item label="Create New Loan" tag="router-link" to="/createLoan"></b-menu-item>
                  <b-menu-item label="Pending" tag="router-link" :to="{ name: 'PendingLoans'}"></b-menu-item>
                  <b-menu-item label="Approved" tag="router-link" :to="{ name: 'ApprovedLoans'}"></b-menu-item>
                  <b-menu-item label="Declined" tag="router-link" :to="{ name: 'DeclinedLoans'}"></b-menu-item>
                </b-menu-item>
                <!-- <b-menu-item icon="money-bill-wave" label="Create CA"></b-menu-item> -->
                <b-menu-item icon="user-plus" label="New Client" tag="router-link" :to="{ name: 'CreateClient'}"></b-menu-item>
                <b-menu-item icon="print">
                  <template #label="props">
                    Financial Statements
                    <b-icon class="is-pulled-right" :icon="props.expanded ? 'caret-up' : 'caret-down'"></b-icon>
                  </template>
                  <b-menu-item label="Cash Flow Statement" tag="router-link" :to="{ name: 'CashFlowStatement'}"></b-menu-item>
                  <!-- <b-menu-item label="Daily General Report"></b-menu-item>
                  <b-menu-item label="Daily Collection"></b-menu-item>
                  <b-menu-item label="Daily Transaction"></b-menu-item> -->
                </b-menu-item>
              </b-menu-list>
            </b-menu>
        </div>
        <div class="column">
          <div class="box">
            <router-view/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

#canvas {
  margin-top: 2.0em;
}

.header {
  margin-bottom: 1.5em;
}

</style>
