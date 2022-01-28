<template>
  <div id="app">
    <b-navbar shadow spaced>
        <template #brand>
            <b-navbar-item>
              <a>
                <h1 class="is-size-5">
                  ION
                  <strong class="is-size-7">Loan Application</strong>
                </h1>
              </a>
            </b-navbar-item>
        </template>

        <template #start>
            <b-navbar-item tag="router-link" :to="{ path: '/clients'}">
                Clients
            </b-navbar-item>
            <b-navbar-dropdown label="Loan" boxed>
                <b-navbar-item tag="router-link" :to="{ path: '/loans/pending'}">
                    Pending
                </b-navbar-item>
                <b-navbar-item tag="router-link" :to="{ path: '/loans/approved'}">
                    Approved
                </b-navbar-item>
                <!-- <b-navbar-item href="#">
                    Declined
                </b-navbar-item> -->
            </b-navbar-dropdown>
            <b-navbar-dropdown label="Financial Statements" boxed>
                <b-navbar-item tag="router-link" :to="{ path: '/cashFlowStatement'}">
                  Daily Cash Flow Statement
                </b-navbar-item>
                <b-navbar-item tag="router-link" :to="{ path: '/rangedCashFlowStatement'}">
                  Date Ranged Cash Flow Statement
                </b-navbar-item>
            </b-navbar-dropdown>
            <b-navbar-dropdown label="Create Actions" boxed>
              <b-navbar-item tag="router-link" :to="{ path: '/createClient'}">
                  Create Client
              </b-navbar-item>
              <b-navbar-item tag="router-link" :to="{ path: '/createLoan'}">
                  Create Loan
              </b-navbar-item>
            </b-navbar-dropdown>
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

    <div class="container">
      <div class="main-wrapper">
        <router-view/>
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

#canvas {
  margin-top: 2.0em;
}

.header {
  margin-bottom: 1.5em;
}

.main-wrapper {
  margin-top: 2.5em;
}

.router-link-exact-active, a.navbar-item:focus, a.navbar-item:focus-within, a.navbar-item:hover {
  background: #7957d5 !important;
  color: white !important;
}

nav a {
  margin-right: 0.5em;
}

.navbar-dropdown a {
  margin-right: 0em;
}

</style>
