<template>
  <div id="app">
    <b-navbar shadow spaced>
        <template #brand>
            <b-navbar-item>
                <h1 class="is-size-5">
                  ION
                </h1>
            </b-navbar-item>
        </template>

        <template #start v-if="isAuthenticated">
            <b-navbar-item tag="router-link" :to="{ path: '/'}">
                Dashboard
            </b-navbar-item>
            <b-navbar-dropdown label="Financial Reports" boxed>
                <b-navbar-item tag="router-link" :to="{ path: '/cashFlowStatement'}">
                  Daily Cash Flow Statement
                </b-navbar-item>
                <b-navbar-item tag="router-link" :to="{ path: '/rangedCashFlowStatement'}">
                  Date Ranged Cash Flow Statement
                </b-navbar-item>
            </b-navbar-dropdown>
        </template>
        <template #end v-if="isAuthenticated">
            <b-navbar-item tag="div">
                <div class="buttons">
                    <b-button class="button is-warning is-light" icon-left="sticky-note" @click="journalModal=true">
                        Create Journal Entry
                    </b-button>
                </div>
            </b-navbar-item>
            <b-navbar-item tag="div">
                <div class="buttons">
                    <b-button class="button is-warning is-light" icon-left="calculator" @click="calculatorModal=true">
                        Loan Calculator
                    </b-button>
                </div>
            </b-navbar-item>
            <b-navbar-item tag="div">
                <div class="buttons">
                    <b-button class="button is-warning is-light" @click="signOut()">
                        Log out
                    </b-button>
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
                    <b-field label="Principal Amount*" :label-position="labelPosition">
                        <b-input v-model="sampleLoan.principalAmount" v-mask="currencyMask"></b-input>
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
                <div class="column">
                  <b-field label="Mode of Payment*" :label-position="labelPosition">
                      <b-select placeholder="Select Mode of Payment" expanded v-model="sampleLoan.loan_mode">
                          <option
                              v-for="option in loan_modes"
                              :value="option.value"
                              :key="option.value">
                              {{ option.display }}
                          </option>
                      </b-select>
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
                      <label for="">Amortization</label>
                  </div>
                  <div class="column is-4">
                      <p>------------------------------</p>
                  </div>
                  <div class="column is-4">
                      {{ computedSampleLoan.amortization | displayMoney }}
                  </div>
              </div>
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
              <div class="columns" v-if="sampleLoan.add_fee_others">
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
                  sampleLoan = {is_advance: true, add_fee_others: true};
                }"/>
            </footer>
        </div>
    </b-modal>

    <b-modal v-model="journalModal" :width="640" scroll="keep">
        <div class="modal-card">
            <header class="modal-card-head">
              <p class="modal-card-title">Create Journal Entry</p>
            </header>
            <section class="modal-card-body">
              <div class="columns">
                  <div class="column is-6">
                      <b-field label="Post Date" :label-position="labelPosition">
                          <b-input v-model="newEntry.post_date" placeholder="MM/DD/YYYY" v-mask="'##/##/####'"></b-input>
                      </b-field>
                  </div>
                  <div class="column is-6">
                      <b-field label="Amount" :label-position="labelPosition">
                          <b-input v-model="newEntry.amount" v-mask="currencyMask"></b-input>
                      </b-field>
                  </div>
              </div>
              <div class="columns">
                <div class="column">
                  <b-field label="Transaction Side*" :label-position="labelPosition">
                      <b-select placeholder="Select Side" expanded v-model="newEntry.transaction_side">
                          <option
                              v-for="option in transactionSides"
                              :value="option.value"
                              :key="option.value">
                              {{ option.display }}
                          </option>
                      </b-select>
                  </b-field>
                </div>
                <div class="column">
                  <b-field label="Account" :label-position="labelPosition">
                      <b-select placeholder="Select Account" expanded v-model="newEntry.account">
                          <option
                              v-for="option in accounts"
                              :value="option.value"
                              :key="option.value">
                              {{ option.display }}
                          </option>
                      </b-select>
                  </b-field>
                </div>
              </div>
              <div class="columns">
                  <div class="column is-12">
                      <b-field label="Description" :label-position="labelPosition">
                          <b-input v-model="newEntry.description" maxlength="200" type="textarea"></b-input>
                      </b-field>
                  </div>
              </div>
            </section>
            <footer class="modal-card-foot">
              <b-button
                label="Close"
                @click="() => {
                  journalModal = false;
                  newEntry = {};
                }"/>
              <b-button type="is-success" @click="createJournal()">Submit</b-button>
            </footer>
        </div>
    </b-modal>
    <!-- End Modals -->

    <!-- Loading -->
    <b-loading :is-full-page="true" v-model="isLoading">
      <b-icon
          pack="fas"
          icon="sync-alt"
          size="is-large"
          custom-class="fa-spin">
      </b-icon>
      Processing Request. Please wait.
    </b-loading>
    <!-- End Loading -->
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import createNumberMask from 'text-mask-addons/dist/createNumberMask'
import { createEntry } from '@/api/transaction.js'
import moment from 'moment'

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
      isLoading: false,
      labelPosition: 'inside',
      calculatorModal: false,
      journalModal: false,
      sampleLoan: {is_advance: true, add_fee_others: true, loan_mode: 'monthly'},
      newEntry: {},
      //selectOptions
      transactionSides: [
        {value: 'debit', display: 'Debit'},
        {value: 'credit', display: 'Credit'},
      ],
      loan_modes: [
        {value: 'semi_monthly', display: 'Semi Monthly'},
        {value: 'monthly', display: 'Monthly'},
      ],
      accounts: [
        {value: 'assets', display: 'Assets'},
        {value: 'liabilities', display: 'Liabilities'},
        {value: 'equity', display: 'Equity'},
      ],
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated']),
    computedSampleLoan () {
      if (!!this.sampleLoan.principalAmount && !!this.sampleLoan.term && !!this.sampleLoan.interest && !!this.sampleLoan.loan_mode) {
        const principalAmount = parseInt(this.sampleLoan.principalAmount.replace(/,/g, ''))
        const interestRate = this.sampleLoan.interest * this.sampleLoan.term
        let udi = (principalAmount * interestRate) / 100

        let amortization = principalAmount / this.sampleLoan.term

        if (!this.sampleLoan.is_advance) {
          amortization = (principalAmount + udi) / this.sampleLoan.term
        }

        if (this.sampleLoan.loan_mode === 'semi_monthly') {
          amortization = amortization / 2
        }

        const totalAmount = principalAmount + udi

        let grossCashOut = 0
        const llrf = (principalAmount / 1000) * (parseInt(this.sampleLoan.term) + 1)
        const processingFee = 150
        
        let feeOthers = udi * 0.05

        if (!this.sampleLoan.add_fee_others) {
          feeOthers = 0
        }

        let totalDeductions = llrf + processingFee + feeOthers

        if (this.sampleLoan.is_advance) {
          totalDeductions += udi
          grossCashOut = principalAmount - udi
        } else {
          grossCashOut = principalAmount
        }

        const netCashout = principalAmount  - totalDeductions

        return {
          principalAmount,
          udi,
          totalAmount,
          grossCashOut,
          llrf,
          processingFee,
          feeOthers,
          totalDeductions,
          netCashout,
          amortization
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
        amortization: 0
      }
    }    
  },
  methods: {
    ...mapActions(['logout']),
    signOut () {
      this.logout()
      this.$router.push('/login')
    },
    async createJournal () {
        try {
            this.isLoading = true

            const entry = {...this.newEntry}
            entry.amount = parseFloat(entry.amount.replace(/,/g, ''))
            entry.post_date = moment(entry.post_date).format('YYYY-MM-DD')

            const response = await createEntry(entry)

            this.newEntry = {}
            this.journalModal = false
            this.$buefy.toast.open({
                message: `Journal Entry Created!`,
                type: 'is-success'
            })

        } catch (err) {
            this.$buefy.toast.open({
                message: `Something went wrong: ${err.message}`,
                type: 'is-danger'
            })
        } finally {
          this.isLoading = false
        }
    }
  }
}
</script>

<style>
:root {
  --primary: #D77A61;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.table tr.is-selected {
  background-color: var(--primary) !important;
}

.input:focus, .select select:focus {
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 0.125em rgb(243 119 44 / 28%) !important;
}

.b-table .table:focus {
  border-color: #FFF !important;
  box-shadow: none !important;
}

.tabs li.is-active a {
  color: var(--primary) !important;
}

.select:not(.is-multiple):not(.is-loading)::after {
  border-color: var(--primary) !important;
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
  font-size: 14px;
}

.navbar {
  background-color: #223843 !important;
}

.navbar .navbar-item {
  color: #fff !important;
}


/* .navbar-item.has-dropdown:focus .navbar-link, .navbar-item.has-dropdown:hover .navbar-link, .navbar-item.has-dropdown.is-active .navbar-link {
  background-color: #D77A61 !important;
} */

a.navbar-item:focus, a.navbar-item:hover, a.navbar-link:hover, a.navbar-link:focus, a.navbar-link:active {
  color: #000 !important;
}

/* a.navbar-item:focus, .navbar-dropdown {
  color: #000 !important;
} */
.navbar-dropdown > .navbar-item {
  color: #000 !important;
}

.navbar-link:not(.is-arrowless)::after {
  border-color: #FFF !important;
}

.navbar-link:not(.is-arrowless)::after:hover {
  border-color: #000 !important;
}

.is-warning, .is-info {
  background: #D77A61 !important;
  color: #fff !important;
}

.is-success {
  background: #223843 !important;
  color: #FFF !important;
}

.modal-card-head {
  background-color: var(--primary) !important;
}

.b-checkbox.checkbox input[type=checkbox]:checked + .check {
    background: var(--primary) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1 1'%3E%3Cpath style='fill:%23fff' d='M 0.04038059,0.6267767 0.14644661,0.52071068 0.42928932,0.80355339 0.3232233,0.90961941 z M 0.21715729,0.80355339 0.85355339,0.16715729 0.95961941,0.2732233 0.3232233,0.90961941 z'%3E%3C/path%3E%3C/svg%3E") no-repeat center center !important;
    border-color: var(--primary) !important;
}

.modal-card-title {
    color: #FFF !important;
}

a.navbar-item, a.navbar-link {
  color: #FFF !important;
}

html, body {
    height: 100vh;
    background: #EFF1F3;
}

</style>
