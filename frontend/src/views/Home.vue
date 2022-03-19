<template>
  <div class="home">
    <div class="columns">
      <div class="column is-1">
        <b-button class="button is-success" @click="newClientModal=true">
            New Client
        </b-button>
      </div>
      <div class="column is-1" v-if="selectedClient">
        <b-button class="button is-success" @click="newLoanModal=true">
            New Loan
        </b-button>
      </div>
      <div class="column is-1" v-if="selectedClient">
        <b-button class="button is-success">
            New CA
        </b-button>
      </div>
      <div class="column is-1">
        <b-button class="button is-info" icon-left="calculator" @click="calculatorModal=true">
            Loan Calculator
        </b-button>
      </div>      
    </div>
    <div class="tile is-ancestor">
      <div class="tile is-vertical is-12">
        <div class="tile">
          <div class="tile is-parent is-vertical">
            <div class="tile is-child box">
              <ClientSelector v-on:client-selected="onClientSelected"/>
              <div class="px-3 py-3" v-if="selectedClient">
                <div class="columns">
                  <div class="column">
                    <label for="">Pension Amount</label>
                    <p>{{selectedClient.pension}}</p>
                  </div>
                </div>
                <div class="columns">
                  <div class="column">
                    <label for="">SSS Number</label>
                    <p>{{selectedClient.sss_no}}</p>
                  </div>
                </div>
                <div class="columns">
                  <div class="column">
                    <label for="">Bank Name</label>
                    <p>{{selectedClient.bank_name}}</p>
                  </div>
                </div>
                <div class="columns">
                  <div class="column">
                    <label for="">Account Number</label>
                    <p>{{selectedClient.account_number}}</p>
                  </div>
                </div>
                <div class="columns">
                  <div class="column">
                    <label for="">Co-Maker Full Name</label>
                    <p>{{selectedClient.co_maker}}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="tile is-parent">
            <div class="tile is-child box" id="computation-table">
              <p class="is-size-4">Collections</p>
            </div>
          </div>
        </div>
        <div class="tile is-parent">
          <div class="tile is-child box">
            <p class="is-size-4">Loans and CAs</p>
              <b-table :data="selectedClient.active_loan_headers" :columns="loanColumns" :selected.sync="selectedLoan" focusable v-if="selectedClient">
                  <template #empty>
                      <div class="has-text-centered">No Results Found</div>
                  </template>
              </b-table>
          </div>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <b-modal v-model="newClientModal" :width="640" scroll="keep">
        <div class="modal-card">
            <header class="modal-card-head">
              <p class="modal-card-title">New Client</p>
            </header>
            <section class="modal-card-body">
              <div class="columns">
                <div class="column">
                  <b-field label="First Name*" :label-position="labelPosition">
                      <b-input v-model="newClient.first_name"></b-input>
                  </b-field>
                </div>
                <div class="column">
                    <b-field label="Middle Name" :label-position="labelPosition">
                        <b-input v-model="newClient.middle_name"></b-input>
                    </b-field>
                </div>
                <div class="column">
                    <b-field label="Last Name*" :label-position="labelPosition">
                        <b-input v-model="newClient.last_name"></b-input>
                    </b-field>
                </div>
              </div>
              <div class="columns">
                <div class="column is-12">
                    <b-field label="Address*" :label-position="labelPosition">
                        <b-input v-model="newClient.address"></b-input>
                    </b-field>
                </div>
              </div>
              <div class="columns">
                <div class="column">
                    <b-field label="Contact No*" :label-position="labelPosition">
                        <b-input v-model="newClient.contact_number"></b-input>
                    </b-field>
                </div>
                <div class="column">
                  <b-field label="Date of Birth*" :label-position="labelPosition">
                    <b-input v-model="newClient.birth_date"></b-input>
                  </b-field>
                </div>
              </div>
              <div class="columns">
                <div class="column">
                    <b-field label="Bank Name*" :label-position="labelPosition">
                        <b-input v-model="newClient.bank_name"></b-input>
                    </b-field>
                </div>
                <div class="column">
                    <b-field label="Account Number*" :label-position="labelPosition">
                        <b-input v-model="newClient.account_number"></b-input>
                    </b-field>
                </div>
              </div>
              <div class="columns">
                <div class="column">
                    <b-field label="Pension Amount" :label-position="labelPosition">
                        <b-input v-model="newClient.pension"></b-input>
                    </b-field>
                </div>
                <div class="column">
                    <b-field label="SSS Number" :label-position="labelPosition">
                        <b-input v-model="newClient.sss_no"></b-input>
                    </b-field>
                </div>
              </div>
              <div class="columns">
                  <div class="column">
                      <b-field label="Co-Maker Full Name" :label-position="labelPosition">
                          <b-input v-model="newClient.co_maker"></b-input>
                      </b-field>
                  </div>
              </div>
            </section>
            <footer class="modal-card-foot">
              <b-button
                label="Cancel"
                @click="() => {
                  newClientModal = false;
                  newClient = {};
                }"/>
              <b-button
                label="Submit"
                type="is-success"
                @click="createClient()"/>
            </footer>
        </div>
    </b-modal>

    <b-modal v-model="newLoanModal" :width="640" scroll="keep">
        <div class="modal-card">
            <header class="modal-card-head">
              <p class="modal-card-title">New Loan</p>
            </header>
            <section class="modal-card-body">
              <div class="columns">
                <div class="column">
                    <b-field label="Principal Amount" :label-position="labelPosition">
                        <b-input v-model="newLoan.principal_amount"></b-input>
                    </b-field>
                </div>
                <div class="column">
                    <b-field label="Term in Months" :label-position="labelPosition">
                        <b-input v-model="newLoan.term"></b-input>
                    </b-field>
                </div>
              </div>
              <div class="columns">
                <div class="column">
                    <b-field label="Interest (%)" :label-position="labelPosition">
                        <b-input v-model="newLoan.interest"></b-input>
                    </b-field>
                </div>
                <div class="column">
                  <b-field label="Loan Type" :label-position="labelPosition">
                      <b-select placeholder="Select a loan type" expanded v-model="newLoan.loan_type">
                          <option
                              v-for="option in loanTypes"
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
                    <b-field label="Payment Start Date" :label-position="labelPosition">
                        <b-input v-model="newLoan.start_payment" placeholder="MM/DD/YYYY"></b-input>
                    </b-field>
                </div>
                <div class="column">
                    <b-field label="Control Number" :label-position="labelPosition">
                        <b-input v-model="newLoan.control_number"></b-input>
                    </b-field>
                </div>
              </div>
              <div class="columns">
                <div class="column is-offset-6">
                  <b-checkbox v-model="newLoan.is_advance">Advanced</b-checkbox>
                </div>
              </div>
            </section>
            <footer class="modal-card-foot">
              <b-button
                label="Cancel"
                @click="() => {
                  newLoanModal = false;
                  newLoan = {};
                }"/>
              <b-button
                label="Submit"
                type="is-success"
                @click="createLoan()"/>
            </footer>
        </div>
    </b-modal>

    <b-modal v-model="calculatorModal" :width="640" scroll="keep">
        <div class="modal-card">
            <header class="modal-card-head">
              <p class="modal-card-title">Loan Calculator</p>
            </header>
            <section class="modal-card-body">
              <div class="columns">
                <div class="column">
                    <b-field label="Desired Amortization*" :label-position="labelPosition">
                        <b-input v-model="sampleLoan.amortization"></b-input>
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
                  sampleLoan = {};
                }"/>
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
import ClientSelector from '@/components/ClientSelector.vue';
import moment from 'moment';

const toCurrency = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'PHP'
})

export default {
  name: 'Home',
  components: {
    ClientSelector
  },
  filters: {
    displayMoney(value) {
      return toCurrency.format(value)
    },
  },
  data() {
    return {
      labelPosition: 'inside',
      selectedClient: null,
      selectedLoan: null,
      isLoading: false,

      // models
      newClient: {},
      newLoan: {},
      sampleLoan: {is_advance: false},

      // modals
      newClientModal: false,
      newLoanModal: false,
      newCAModal: false,
      calculatorModal: false,

      //selectOptions
      loanTypes: [
        {value: 'pension', display: 'Pension'},
        {value: 'salary', display: 'Salary'},
      ],

      // columns
      loanColumns: [
          {
              field: 'control_number',
              label: 'Control Number'
          },
          {
              field: 'principal_amount',
              label: 'Principal Amount'
          },
          {
              field: 'term',
              label: 'Terms (Months)'
          },
          {
              field: 'interest',
              label: 'Interest'
          },
          {
              field: 'running_balance',
              label: 'Running Balance'
          },
      ],
      computationColumns: [
          {
              field: 'number',
              label: '#'
          },
          {
              field: 'payment_date',
              label: 'Payment Date'
          },
          {
              field: 'amount',
              label: 'Amount',
          },
      ],
    }
  },
  methods: {
    onClientSelected (value) {
      this.selectedClient = value
    },
    createClient () {
      this.isLoading = true
    },
    createLoan () {
      this.isLoading = true
    }
  },
  computed: {
    loanDetails () {
      if (this.selectedLoan) {
        return this.selectedLoan.loan_detail.map((item, index) => {
          return {
            ...item,
            number: index + 1,
            payment_date: moment(item.date_payment).format('MM/DD/YYYY'),
          }
        })
      }

      return []
    },
    computedSampleLoan () {
      if (!!this.sampleLoan.amortization && !!this.sampleLoan.term && !!this.sampleLoan.interest) {

        const principalAmount = this.sampleLoan.amortization * this.sampleLoan.term
        const interestRate = this.sampleLoan.interest * this.sampleLoan.term
        const udi = (principalAmount * interestRate) / 100
        const totalAmount = principalAmount + udi
        const grossCashOut = principalAmount - udi
        const llrf = (principalAmount / 1000) * (this.sampleLoan.term + 1)
        const processingFee = 150
        const feeOthers = udi * 0.05

        let totalDeductions = 0

        if (this.sampleLoan.is_advance) {
          totalDeductions = llrf + processingFee + udi + feeOthers
        } else {
          totalDeductions = llrf + processingFee + feeOthers
        }

        const netCashout = principalAmount - totalDeductions

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
  }
}
</script>

<style>
  .home {
    text-align: initial;
  }

  #computation-table {
    max-height: 500px;
    overflow: scroll;
  }
</style>