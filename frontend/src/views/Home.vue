<template>
  <div class="home">
    <div class="columns">
      <div class="column is-1">
        <b-button class="button is-info is-light" @click="newClientModal=true" rounded>
            New Client
        </b-button>
      </div>
      <div class="column is-1" v-if="selectedClient">
        <b-button class="button is-info is-light" @click="newLoanModal=true" rounded>
            New Loan
        </b-button>
      </div>
      <div class="column is-1" v-if="selectedClient">
        <b-button class="button is-info is-light" rounded>
            New CA
        </b-button>
      </div>     
    </div>
    <div class="tile is-ancestor">
      <div class="tile is-vertical is-12">
        <div class="tile">
          <div class="tile is-parent is-vertical is-4">
            <div class="tile is-child box notification is-success is-light">
              <ClientSelector v-on:client-selected="onClientSelected"/>
              <div class="px-3 py-3" v-if="selectedClient">
                <div class="columns">
                  <div class="column">
                    <label for="">Pension Amount</label>
                    <p>{{selectedClient.pension | displayMoney}}</p>
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
              <b-table :data="collections" narrowed striped>
                <b-table-column field="reference_code" label="Ref Code" v-slot="props">
                  {{ props.row.reference_code }}
                </b-table-column>
                <b-table-column field="collection_amount" label="Amount" v-slot="props">
                  {{ props.row.collection_amount | displayMoney }}
                </b-table-column>
                <b-table-column field="post_date" label="Payment Date" v-slot="props">
                  {{ props.row.post_date | shortDate }}
                </b-table-column>
                <b-table-column field="refundable_amount" label="AP" v-slot="props">
                  {{ props.row.refundable_amount | displayMoney }}
                </b-table-column>
                <b-table-column field="actions" label="Actions" centered v-slot="props">
                  <b-button class="is-success is-light is-small" v-if="props.row.refundable_amount">Pay Refund</b-button>
                  &nbsp;
                  <b-button class="is-small" @click="showCollectionDetail(props.row.collection_details)">Details</b-button>
                </b-table-column>
                <template #empty>
                  <div class="has-text-centered">No Results Found</div>
                </template>
              </b-table>              
            </div>
          </div>
        </div>
        <div class="tile is-parent">
          <div class="tile is-child box">
              <!-- <div class="columns">
                <div class="column">
                  <p class="is-size-4">Loans and CAs</p>
                </div>
              </div> -->
              <div class="columns" v-if="selectedLoanRows.length > 0">
                  <div class="column is-2">
                      <b-field label="Reference" :label-position="labelPosition">
                          <b-input v-model="newCollection.reference_code"></b-input>
                      </b-field>
                  </div>
                  <div class="column is-2">
                      <b-field label="Amount" :label-position="labelPosition">
                          <b-input v-model="newCollection.amount" v-mask="currencyMask"></b-input>
                      </b-field>
                  </div>
                  <div class="column is-2">
                      <b-field label="Date" :label-position="labelPosition">
                          <b-input v-model="newCollection.post_date" v-mask="'##/##/####'" placeholder="MM/DD/YYYY"></b-input>
                      </b-field>
                  </div>
                  <div class="column is-2">
                      <b-button
                          label="Create Collection"
                          type="is-info"
                          size="is-medium"
                          :disabled="canCreateCollection"
                          @click="confirmCreateCollection" />
                  </div>
              </div>

              <b-table :data="loans" :selected.sync="selectedLoan" focusable checkable :checked-rows.sync="selectedLoanRows" narrowed striped>
                <b-table-column field="control_number" label="Loan Control Number" v-slot="props">
                  {{ props.row.control_number }}
                </b-table-column>
                <b-table-column field="principal_amount" label="Principal Amount" v-slot="props">
                  {{ props.row.principal_amount | displayMoney }}
                </b-table-column>
                <b-table-column field="amortization" label="Amortization" v-slot="props">
                  {{ props.row.amortization | displayMoney }}
                </b-table-column>
                <b-table-column field="term" label="Term in Months" v-slot="props">
                  {{ props.row.term}}
                </b-table-column>
                <b-table-column field="interest" label="Interest %" v-slot="props">
                  {{ props.row.interest}}
                </b-table-column>
                <b-table-column field="running_balance" label="Running Balance" v-slot="props">
                  {{ props.row.running_balance |displayMoney }}
                </b-table-column>
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
                    <b-input v-mask="'##/##/####'" v-model="newClient.birth_date" placeholder="MM/DD/YYYY"></b-input>
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
                    <b-field label="Pension Amount*" :label-position="labelPosition">
                        <b-input v-mask="currencyMask" v-model="newClient.pension"></b-input>
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
                        <b-input v-mask="currencyMask" v-model="newLoan.principal_amount"></b-input>
                    </b-field>
                </div>
                <div class="column">
                    <b-field label="Term in Months" :label-position="labelPosition">
                        <b-input v-model="newLoan.term" type="number"></b-input>
                    </b-field>
                </div>
              </div>
              <div class="columns">
                <div class="column">
                    <b-field label="Interest (%)" :label-position="labelPosition">
                        <b-input v-mask="currencyMask" v-model="newLoan.interest"></b-input>
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
                        <b-input v-mask="'##/##/####'" v-model="newLoan.start_payment" placeholder="MM/DD/YYYY"></b-input>
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


    <b-modal v-model="collectionDetailModal" :width="640" scroll="keep">
        <div class="modal-card">
            <header class="modal-card-head">
              <p class="modal-card-title">Collection Detail</p>
            </header>
            <section class="modal-card-body">
              <b-table :data="collectionDetails" narrowed striped>
                <b-table-column field="control_number" label="Control Number" v-slot="props">
                  {{ props.row.loan.control_number }}
                </b-table-column>
                <b-table-column field="amount_used" label="Amount" v-slot="props">
                  {{ props.row.amount_used | displayMoney }}
                </b-table-column>
                <template #empty>
                  <div class="has-text-centered">No Results Found</div>
                </template>
              </b-table>
            </section>
            <footer class="modal-card-foot">
              <b-button
                label="Close"
                @click="() => {
                  collectionDetailModal = false
                  collectionDetails = []
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
import createNumberMask from 'text-mask-addons/dist/createNumberMask'

// endpoints
import { createClient } from '@/api/client.js'
import { createLoan } from '@/api/loan.js'
import { approveLoan, searchLoans } from '@/api/loan.js'
import { createCollection, fetchCollections } from '@/api/collection.js'

const currencyMask = createNumberMask({
  prefix: '',
  allowDecimal: true,
  includeThousandsSeparator: true,
  allowNegative: false,
});

export default {
  name: 'Home',
  components: {
    ClientSelector
  },
  data() {
    return {
      currencyMask,
      labelPosition: 'inside',
      selectedClient: null,
      selectedLoan: null,
      isLoading: false,

      // models
      newClient: {},
      newLoan: {},
      loans: [],
      selectedLoanRows: [],
      newCollection: {},
      collections: [],
      collectionDetails: [],

      // modals
      newClientModal: false,
      newLoanModal: false,
      newCAModal: false,
      collectionDetailModal : false,

      //selectOptions
      loanTypes: [
        {value: 'pension', display: 'Pension'},
        {value: 'salary', display: 'Salary'},
      ],

      // columns
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
      this.fetchLoans()
      this.fetchPayments()
    },
    showCollectionDetail (collectionDetails) {
      this.collectionDetails = collectionDetails
      this.collectionDetailModal = true
    },
    generateCollectionMessage() {
        return `Posting Collection for Loans: <br/>
        ${this.selectedLoanRows.map(loan => (`<b>${loan.control_number}</b>`))}
        `
    },
    confirmCreateCollection () {
      this.$buefy.dialog.confirm({
          title: 'Creating Collection',
          message: this.generateCollectionMessage(),
          confirmText: 'Create Collection',
          type: 'is-info',
          hasIcon: true,
          onConfirm: () => this.createCollection()
      })
    },
    async createCollection() {
        try {
            this.isLoading = true
            const collection = {
              ...this.newCollection,
              post_date: moment(this.newCollection.post_date).format('YYYY-MM-DD'),
              collection_amount: parseFloat(this.newCollection.amount.replace(/,/g, '')),
              selected_loans: this.selectedLoanRows.map(loan => (loan.id)),
              client: this.selectedClient.id
            }

            await createCollection({
                ...collection,
            })

            this.selectedLoanRows = []
            this.newCollection = {}
            this.$buefy.toast.open({
                message: 'Collection Successfully Posted!',
                type: 'is-success'
            })
            this.fetchLoans()
            this.fetchPayments()
        } catch (err) {
            this.$buefy.toast.open({
                message: `Something went wrong! ${err.message}`,
                type: 'is-danger'
            })
        } finally {
            this.isLoading = false
        }
    },
    async createClient () {
      try {
        this.isLoading = true

        const client = {...this.newClient}
        client.pension = parseFloat(this.newClient.pension.replace(/,/g, ''))
        const response = await createClient(client)

        this.$buefy.toast.open({
          message: `Client Successfully Created!`,
          type: 'is-success'
        })

        this.newClientModal = false
        this.newClient = {}
      } catch (err) {
        this.$buefy.toast.open({
          message: `Something went wrong: ${err.message}`,
          type: 'is-danger'
        })
      } finally {
        this.isLoading = false
      }
    },
    async createLoan () {
      try {
        this.isLoading = true

        const loan = {...this.newLoan}
        loan.start_payment = moment(loan.start_payment).format('YYYY-MM-DD')
        loan.maturity_date = moment(loan.start_payment).add(loan.term - 1, 'months').format('YYYY-MM-DD')
        loan.principal_amount = parseFloat(loan.principal_amount.replace(/,/g, ''))

        const response = await createLoan({
            ...loan,
            client: this.selectedClient.id
        })

        await approveLoan(response.data.id)

        this.$buefy.toast.open({
            message: 'Loan Created Successfully!',
            type: 'is-success'
        })
        this.newLoanModal = false
        this.newLoan = {}
        this.fetchLoans()
      } catch (err) {
        this.$buefy.toast.open({
          message: `Something went wrong: ${err.message}`,
          type: 'is-danger'
        })
      } finally {
        this.isLoading = false
      }
    },
    async fetchLoans () {
      if (!this.selectedClient) {
        this.loans = []
        return
      }

      try {
        this.isLoading = true
        const response = await searchLoans({client_id: this.selectedClient.id})

        this.loans = response.data
      } catch (err) {
        console.log('Unable to fetch loans:', err)
        this.loans = []
      } finally {
        this.isLoading = false
      }
    },
    async fetchPayments () {
      if (!this.selectedClient) {
        this.collections = []
        return
      }

      try {
        this.isLoading = true
        const response = await fetchCollections({client_id: this.selectedClient.id})

        this.collections = response.data
      } catch (err) {
        console.log('Unable to fetch collections:', err)
        this.collections = []
      } finally {
        this.isLoading = false
      }
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
    canCreateCollection() {
        if (!!this.newCollection.amount && !!this.newCollection.reference_code && !!this.newCollection.post_date) {
            return false
        }

        return true
    },
  },
  watch: {
    selectedLoanRows(newSelectedLoanRows, _) {
      if (newSelectedLoanRows.length === 0) {
        this.newCollection = {}
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