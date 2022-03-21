<template>
  <div id="app">
    <b-navbar shadow spaced>
        <template #brand>
            <b-navbar-item>
              <a>
                <h1 class="is-size-5">
                  ION
                </h1>
              </a>
            </b-navbar-item>
        </template>

        <template #start v-if="isAuthenticated">
            <b-navbar-item tag="router-link" :to="{ path: '/'}">
                Dashboard
            </b-navbar-item>
            <!-- <b-navbar-dropdown label="Loan" boxed>
                <b-navbar-item tag="router-link" :to="{ path: '/loans/pending'}">
                    Pending
                </b-navbar-item>
                <b-navbar-item tag="router-link" :to="{ path: '/loans/approved'}">
                    Approved
                </b-navbar-item>
            </b-navbar-dropdown> -->
            <b-navbar-dropdown label="Financial Statements" boxed>
                <b-navbar-item tag="router-link" :to="{ path: '/cashFlowStatement'}">
                  Daily Cash Flow Statement
                </b-navbar-item>
                <b-navbar-item tag="router-link" :to="{ path: '/rangedCashFlowStatement'}">
                  Date Ranged Cash Flow Statement
                </b-navbar-item>
            </b-navbar-dropdown>
            <!-- <b-navbar-dropdown label="Create Actions" boxed>
              <b-navbar-item tag="router-link" :to="{ path: '/createClient'}">
                  Create Client
              </b-navbar-item>
              <b-navbar-item tag="router-link" :to="{ path: '/createLoan'}">
                  Create Loan
              </b-navbar-item>
              <b-navbar-item tag="router-link" :to="{ path: '/createExpense'}">
                  Create Expense
              </b-navbar-item>
            </b-navbar-dropdown> -->
        </template>
        <template #end v-if="isAuthenticated">
            <b-navbar-item tag="div">
                <div class="buttons">
                    <b-button class="button is-warning is-light" icon-left="calculator" @click="calculatorModal=true">
                        Loan Calculator
                    </b-button>
                </div>
            </b-navbar-item>
            <b-navbar-item tag="div">
                <div class="buttons">
                    <a class="button is-light" @click="signOut()">
                        Log out
                    </a>
                </div>
            </b-navbar-item>
        </template>
    </b-navbar>

    <div class="container-fluid">
      <div class="main-wrapper">
        <router-view/>
      </div>
    </div>

    <!-- Modals -->
    <b-modal v-model="calculatorModal" :width="640" scroll="keep">
        <div class="modal-card">
            <header class="modal-card-head">
              <p class="modal-card-title">Loan Calculator</p>
            </header>
            <section class="modal-card-body">
              <div class="columns">
                <div class="column">
                    <b-field label="Desired Amortization*" :label-position="labelPosition">
                        <b-input v-model="sampleLoan.amortization" v-mask="currencyMask"></b-input>
                    </b-field>
                </div>
                <div class="column">
                    <b-field label="Term in Months*" :label-position="labelPosition">
                        <b-input v-model="sampleLoan.term"></b-input>
                    </b-field>
                </div>
              </div>
              <div class="columns">
                <div class="column">
                    <b-field label="Interest (%)*" :label-position="labelPosition">
                        <b-input v-model="sampleLoan.interest"></b-input>
                    </b-field>
                </div>
              </div>
              <div class="columns">
                <div class="column">
                  <b-checkbox v-model="sampleLoan.is_advance">Advanced</b-checkbox>
                </div>
              </div>
              <hr>
              <div class="columns">
                  <div class="column is-4">
                      <label for="">Principal Amount</label>
                  </div>
                  <div class="column is-4">
                      <p>------------------------------</p>
                  </div>
                  <div class="column is-4">
                      {{ computedSampleLoan.principalAmount | displayMoney }}
                  </div>
              </div>
              <div class="columns">
                  <div class="column is-4">
                      <label for="">U.D.I</label>
                  </div>
                  <div class="column is-4">
                      <p>------------------------------</p>
                  </div>
                  <div class="column is-4">
                      ( {{ computedSampleLoan.udi | displayMoney }} )
                  </div>
              </div>
              <div class="columns">
                  <div class="column is-4">
                      <label for="">Total Amount of Loan</label>
                  </div>
                  <div class="column is-4">
                      <p>------------------------------</p>
                  </div>
                  <div class="column is-4">
                      {{ computedSampleLoan.totalAmount | displayMoney }}
                  </div>
              </div>
              <div class="columns">
                  <div class="column is-4">
                      <label for="">Gross Cash Out</label>
                  </div>
                  <div class="column is-4">
                      <p>------------------------------</p>
                  </div>
                  <div class="column is-4">
                      {{ computedSampleLoan.grossCashOut | displayMoney }}
                  </div>
              </div>
              <div class="columns">
                  <div class="column is-12">
                      <label for="">LESS Fees:</label>
                  </div>
              </div>
              <div class="columns">
                  <div class="column is-4">
                      <!-- <label class="has-text-right" for="">L.L.R.F</label> -->
                  </div>
                  <div class="column is-4">
                      <label class="has-text-right" for="">L.L.R.F</label>
                  </div>
                  <div class="column is-4">
                      ( {{ computedSampleLoan.llrf | displayMoney }} )
                  </div>
              </div>
              <div class="columns">
                  <div class="column is-4">
                      <!-- <label for="">Processing Fee</label> -->
                  </div>
                  <div class="column is-4">
                      <label for="">Processing Fee</label>
                  </div>
                  <div class="column is-4">
                      ( {{ computedSampleLoan.processingFee | displayMoney }} )
                  </div>
              </div>
              <div class="columns">
                  <div class="column is-4">
                      <!-- <label for="">Processing Fee</label> -->
                  </div>
                  <div class="column is-4">
                      <label for="">Others</label>
                  </div>
                  <div class="column is-4">
                      ( {{ computedSampleLoan.feeOthers | displayMoney }} )
                  </div>
              </div>
              <div class="columns">
                  <div class="column is-4">
                      <label for="">Total Deductions</label>
                  </div>
                  <div class="column is-4">
                      <p>------------------------------</p>
                  </div>
                  <div class="column is-4">
                      ( {{ computedSampleLoan.totalDeductions | displayMoney }} )
                  </div>
              </div>
              <div class="columns">
                  <div class="column is-4">
                      <label for="">Net Cash Out</label>
                  </div>
                  <div class="column is-4">
                      <p>------------------------------</p>
                  </div>
                  <div class="column is-4">
                      {{ computedSampleLoan.netCashout | displayMoney }}
                  </div>
              </div>
            </section>
            <footer class="modal-card-foot">
              <b-button
                label="Close"
                @click="() => {
                  calculatorModal = false;
                  sampleLoan = {is_advance: true};
                }"/>
            </footer>
        </div>
    </b-modal>
    <!-- End Modals -->    
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import createNumberMask from 'text-mask-addons/dist/createNumberMask'

const currencyMask = createNumberMask({
  prefix: '',
  allowDecimal: true,
  includeThousandsSeparator: true,
  allowNegative: false,
});

export default {
  data() {
    return {
      currencyMask,
      labelPosition: 'inside',
      calculatorModal: false,
      sampleLoan: {is_advance: true},
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated']),
    computedSampleLoan () {
      if (!!this.sampleLoan.amortization && !!this.sampleLoan.term && !!this.sampleLoan.interest) {
        // Calculate Principal
        let principalAmount = parseInt(this.sampleLoan.amortization.replace(/,/g, '')) * this.sampleLoan.term
        const interestRate = this.sampleLoan.interest * this.sampleLoan.term
        let udi = (principalAmount * interestRate) / 100

        if (!this.sampleLoan.is_advance) {
          principalAmount = (parseInt(this.sampleLoan.amortization.replace(/,/g, '')) * this.sampleLoan.term) - udi
          udi = (principalAmount * interestRate) / 100
        }

        const totalAmount = principalAmount + udi
        let grossCashOut = 0
        const llrf = (principalAmount / 1000) * (this.sampleLoan.term + 1)
        const processingFee = 150
        const feeOthers = udi * 0.05

        let totalDeductions = 0

        if (this.sampleLoan.is_advance) {
          grossCashOut = principalAmount - udi
          totalDeductions = llrf + processingFee + udi + feeOthers
        } else {
          grossCashOut = principalAmount
          totalDeductions = llrf + processingFee + feeOthers
        }

        const netCashout = grossCashOut - totalDeductions

        return {
          principalAmount,
          udi,
          totalAmount,
          grossCashOut,
          llrf,
          processingFee,
          feeOthers,
          totalDeductions,
          netCashout
        }
      }

      return {
        principalAmount: 0,
        udi: 0,
        totalAmount: 0,
        grossCashOut: 0,
        llrf: 0,
        processingFee: 0,
        feeOthers: 0,
        totalDeductions: 0,
        netCashout: 0,
      }
    }    
  },
  methods: {
    ...mapActions(['logout']),
    signOut () {
      this.logout()
      this.$router.push('/login')
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

#canvas {
  margin-top: 2.0em;
}

.header {
  margin-bottom: 1.5em;
}

.main-wrapper {
  margin-top: 1.5em;
  padding-top: 0;
  padding: 1.5em;
}

</style>
