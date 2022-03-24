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
            <b-navbar-dropdown label="Financial Reports" boxed>
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
              </div>
              <div class="columns">
                <div class="column">
                  <b-checkbox v-model="sampleLoan.is_advance">Advanced</b-checkbox>
                </div>
                <div class="column">
                  <b-checkbox v-model="sampleLoan.add_fee_others">Fee Others?</b-checkbox>
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
      journalModal: false,
      sampleLoan: {is_advance: true, add_fee_others: true},
      newEntry: {},
      //selectOptions
      transactionSides: [
        {value: 'debit', display: 'Debit'},
        {value: 'credit', display: 'Credit'},
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
      if (!!this.sampleLoan.principalAmount && !!this.sampleLoan.term && !!this.sampleLoan.interest) {
        const principalAmount = parseInt(this.sampleLoan.principalAmount.replace(/,/g, ''))
        const interestRate = this.sampleLoan.interest * this.sampleLoan.term
        let udi = (principalAmount * interestRate) / 100
        let amortization = principalAmount / this.sampleLoan.term

        if (!this.sampleLoan.is_advance) {
          amortization = (principalAmount + udi) / this.sampleLoan.term
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
