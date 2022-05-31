<template>
  <div class="home">
    <div class="columns">
      <div class="column is-1">
        <b-button class="button is-info is-light" @click="newClientModal=true" expanded>
            New Client
        </b-button>
      </div>
      <div class="column is-1" v-if="selectedClient">
        <b-button class="button is-info is-light" @click="newLoanModal=true" expanded>
            New Loan
        </b-button>
      </div>
      <div class="column is-1" v-if="selectedClient">
        <b-button class="button is-info is-light" @click="newCAModal=true" expanded>
            New CA
        </b-button>
      </div>
    </div>
    <div class="tile is-ancestor">
      <div class="tile is-vertical is-12">
        <div class="tile">
          <div class="tile is-parent is-vertical is-5">
            <div class="tile is-child box">
              <div class="columns">
                <div class="column">
                  <ClientSelector v-on:client-selected="onClientSelected"/>
                </div>
                <div class="column is-3" v-if="selectedClient">
                  <b-button class="button is-info is-light is-medium" @click="editClient" expanded>
                      Edit Client
                  </b-button>
                </div>
              </div>
              <div class="px-3 py-3" v-if="selectedClient">
                <div class="columns">
                  <div class="column" id="first-section-client">
                    <div class="columns">
                      <div class="column">
                        <label for="">Birthdate</label>
                        <p>{{ selectedClient.birth_date | shortDate }}</p>
                      </div>
                      <div class="column">
                        <label for="">Age</label>
                        <p>{{ selectedClient.birth_date | getAge }}</p>
                      </div>
                    </div>
                    <div class="columns">
                      <div class="column">
                        <label for="">Pension Amount</label>
                        <p>{{selectedClient.pension | displayMoney}}</p>
                      </div>
                      <div class="column">
                        <label for="">Potential AP</label>
                        <p>{{clientPotentialAP | displayMoney}}</p>
                      </div>
                    </div>
                    <div class="columns">
                      <div class="column">
                        <label for="">SSS Number</label>
                        <p>{{selectedClient.sss_no}}</p>
                      </div>
                      <div class="column">
                        <label for="">Classification</label>
                        <p>{{selectedClient.classification}}</p>
                      </div>
                    </div>
                    <div class="columns">
                      <div class="column">
                        <label for="">Bank Name</label>
                        <p>{{selectedClient.bank_name}}</p>
                      </div>
                      <div class="column" v-if="selectedClient.classification === 'pension'">
                        <label for="">Pensioner Category</label>
                        <p>{{selectedClient.pension_type}}</p>
                      </div>
                    </div>
                    <div class="columns">
                      <div class="column">
                        <label for="">Account Number</label>
                        <p>{{selectedClient.account_number}}</p>
                      </div>
                      <div class="column">
                        <label for="">Contact Number</label>
                        <p>{{ selectedClient.contact_number }}</p>
                      </div>
                    </div>
                    <div class="columns">
                      <div class="column">
                        <label for="">Address</label>
                        <p>{{selectedClient.address}}</p>
                      </div>
                    </div>
                    <div class="columns">
                      <div class="column">
                        <label for="">Spouse</label>
                        <p>{{selectedClient.spouse_name}}</p>
                      </div>
                    </div>
                    <div class="columns">
                      <div class="column">
                        <label for="">Date of Birth</label>
                        <p>{{selectedClient.spouse_dob}}</p>
                      </div>
                      <div class="column">
                        <label for="">Date of Death</label>
                        <p>{{ selectedClient.spouse_dod }}</p>
                      </div>
                    </div>
                  </div>
                  <div class="column">
                    <div class="columns">
                      <div class="column">
                        <p class="is-size-6 has-text-weight-bold">Dependents</p>
                      </div>
                    </div>
                    <div class="columns">
                      <div class="column">
                        <ul>
                          <li class="my-3" v-if="selectedClient.dependent_1_name">
                            <p>{{ selectedClient.dependent_1_name }}</p>
                            <p>{{ selectedClient.dependent_1_dob }}</p>
                          </li>
                          <li class="my-3" v-if="selectedClient.dependent_2_name">
                            <p>{{ selectedClient.dependent_2_name }}</p>
                            <p>{{ selectedClient.dependent_2_dob }}</p>
                          </li>
                          <li class="my-3" v-if="selectedClient.dependent_3_name">
                            <p>{{ selectedClient.dependent_3_name }}</p>
                            <p>{{ selectedClient.dependent_3_dob }}</p>
                          </li>
                          <li class="my-3" v-if="selectedClient.dependent_4_name">
                            <p>{{ selectedClient.dependent_4_name }}</p>
                            <p>{{ selectedClient.dependent_4_dob }}</p>
                          </li>
                          <li class="my-3" v-if="selectedClient.dependent_5_name">
                            <p>{{ selectedClient.dependent_5_name }}</p>
                            <p>{{ selectedClient.dependent_5_dob }}</p>
                          </li>
                        </ul>
                      </div>
                    </div>
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
                <b-table-column field="collection_amount" label="Amount Collected" v-slot="props">
                  {{ props.row.collection_amount | displayMoney }}
                </b-table-column>
                <b-table-column field="collection_amount" label="Total Amount Used" v-slot="props">
                  {{ calculateCollectionTotal(props.row.collection_details) | displayMoney }}
                </b-table-column>                
                <b-table-column field="post_date" label="Payment Date" v-slot="props">
                  {{ props.row.post_date | shortDate }}
                </b-table-column>
                <b-table-column field="refundable_amount" label="AP" v-slot="props">
                  {{ props.row.refundable_amount | displayMoney }}
                </b-table-column>
                <b-table-column field="actions" label="Actions" centered v-slot="props">
                  <b-button class="is-success is-light is-small" v-if="!props.row.is_refunded" @click="openRefund(props.row)">Pay Refund</b-button>
                  &nbsp;
                  <b-button class="is-small" @click="showCollectionDetail(props.row.collection_details)">Details</b-button>
                  &nbsp;
                  <b-button type="is-danger is-small" icon-right="trash" @click="confirmCollectionDelete(props.row)"/>
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

              <b-table :data="loans" :selected.sync="selectedLoan" focusable checkable :checked-rows.sync="selectedLoanRows" narrowed striped
                :is-row-checkable="(row) => row.running_balance != 0"
                >
                <b-table-column field="control_number" label="LCN" v-slot="props">
                  {{ props.row.control_number }}
                </b-table-column>
                <b-table-column field="date_granted" label="Date Granted" v-slot="props">
                  {{ props.row.date_granted | shortDate }}
                </b-table-column>
                <b-table-column field="start_payment" label="First Deduction" v-slot="props">
                  {{ props.row.start_payment | shortDate }}
                </b-table-column>
                <b-table-column field="maturity_date" label="Maturity Date" v-slot="props">
                  {{ props.row.maturity_date | shortDate }}
                </b-table-column>
                <b-table-column field="term" label="Term" v-slot="props">
                  {{ props.row.term}}
                </b-table-column>
                <b-table-column field="is_advance" label="Advance" v-slot="props">
                  <b-icon icon="check" size="is-small" v-if="props.row.is_advance"></b-icon>
                  <b-icon icon="times" size="is-small" v-else></b-icon>
                </b-table-column>
                <b-table-column field="interest" label="Int %" v-slot="props">
                  {{ props.row.interest}}
                </b-table-column>
                <b-table-column field="principal_amount" label="Princp. Amt" v-slot="props">
                  {{ props.row.principal_amount | displayMoney }}
                </b-table-column>
                <b-table-column field="udi" label="UDI" v-slot="props">
                  {{ props.row.udi | displayMoney }}
                </b-table-column>
                <b-table-column field="amortization" label="Inst." v-slot="props">
                  {{ props.row.amortization | displayMoney }}
                </b-table-column>
                <b-table-column field="llrf" label="L.L.R.F" v-slot="props">
                  {{ props.row.llrf | displayMoney }}
                </b-table-column>
                <b-table-column field="processing_fee" label="P.Fee" v-slot="props">
                  {{ props.row.processing_fee | displayMoney }}
                </b-table-column>
                <b-table-column field="others" label="Others" v-slot="props">
                  {{ props.row.fee_others |displayMoney }}
                </b-table-column>
                <b-table-column field="net_cash_out" label="Net Cash Out" v-slot="props">
                  {{ props.row.net_cash_out | displayMoney }}
                </b-table-column>
                <b-table-column field="running_balance" label="Running Balance" v-slot="props">
                  {{ props.row.running_balance |displayMoney }}
                </b-table-column>
                <template #footer>
                    <th>
                        <div class="th-wrap">
                            <h1 class="is-size-6 has-text-weight-bold">TOTALS</h1>
                        </div>
                    </th>
                    <th></th>
                    <th></th>
                    <th></th>
                    <th></th>
                    <th></th>
                    <th></th>
                    <th></th>
                    <th></th>
                    <th></th>
                    <th>
                      <h1 class="is-size-6 has-text-weight-bold">{{ totalAmortization | displayMoney }}</h1>
                    </th>
                    <th></th>
                    <th></th>
                    <th></th>
                    <th>
                      <h1 class="is-size-6 has-text-weight-bold">{{ loanTotalNetCashOut | displayMoney }}</h1>
                    </th>
                    <th>
                        <h1 class="is-size-6 has-text-weight-bold">{{ loanTotalRunningBalance | displayMoney }}</h1>
                    </th>
                </template>
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
                    <b-field label="Contact No" :label-position="labelPosition">
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
                  <b-field label="Classification*" :label-position="labelPosition">
                      <b-select placeholder="Select Classification" expanded v-model="newClient.classification">
                          <option
                              v-for="option in classifications"
                              :value="option.value"
                              :key="option.value">
                              {{ option.display }}
                          </option>
                      </b-select>
                  </b-field>
                </div>
                <div class="column">
                  <b-field label="Pensioner Category" :label-position="labelPosition">
                      <b-select placeholder="Select Category if Pensioner" expanded v-model="newClient.pension_type">
                          <option
                              v-for="option in pensionCategories"
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
                    <b-field label="Pension/Income Amount*" :label-position="labelPosition">
                        <b-input v-mask="currencyMask" v-model="newClient.pension"></b-input>
                    </b-field>
                </div>
                <div class="column">
                    <b-field label="SSS Number" :label-position="labelPosition">
                        <b-input v-model="newClient.sss_no"></b-input>
                    </b-field>
                </div>
              </div>
              <hr>
              <div class="columns">
                <div class="column">
                  <b-field label="Spouse Name" :label-position="labelPosition">
                      <b-input v-model="newClient.spouse_name"></b-input>
                  </b-field>
                </div>
              </div>
              <div class="columns">
                <div class="column">
                  <b-field label="Spouse Date of Birth" :label-position="labelPosition">
                      <b-input v-mask="'##/##/####'" v-model="newClient.spouse_dob" placeholder="MM/DD/YYYY"></b-input>
                  </b-field>
                </div>
                <div class="column">
                  <b-field label="Spouse Date of Death" :label-position="labelPosition">
                    <b-input v-mask="'##/##/####'" v-model="newClient.spouse_dod" placeholder="MM/DD/YYYY"></b-input>
                  </b-field>
                </div>
              </div>
              <div class="columns">
                <div class="column">
                  <b-field label="Dependent Name" :label-position="labelPosition">
                      <b-input v-model="newClient.dependent_1_name"></b-input>
                  </b-field>
                </div>
                <div class="column">
                  <b-field label="Birthdate" :label-position="labelPosition">
                    <b-input v-mask="'##/##/####'" v-model="newClient.dependent_1_dob" placeholder="MM/DD/YYYY"></b-input>
                  </b-field>
                </div>
              </div>
              <div class="columns">
                <div class="column">
                  <b-field label="Dependent Name" :label-position="labelPosition">
                      <b-input v-model="newClient.dependent_2_name"></b-input>
                  </b-field>
                </div>
                <div class="column">
                  <b-field label="Birthdate" :label-position="labelPosition">
                    <b-input v-mask="'##/##/####'" v-model="newClient.dependent_2_dob" placeholder="MM/DD/YYYY"></b-input>
                  </b-field>
                </div>
              </div>
              <div class="columns">
                <div class="column">
                  <b-field label="Dependent Name" :label-position="labelPosition">
                      <b-input v-model="newClient.dependent_3_name"></b-input>
                  </b-field>
                </div>
                <div class="column">
                  <b-field label="Birthdate" :label-position="labelPosition">
                    <b-input v-mask="'##/##/####'" v-model="newClient.dependent_3_dob" placeholder="MM/DD/YYYY"></b-input>
                  </b-field>
                </div>
              </div>
              <div class="columns">
                <div class="column">
                  <b-field label="Dependent Name" :label-position="labelPosition">
                      <b-input v-model="newClient.dependent_4_name"></b-input>
                  </b-field>
                </div>
                <div class="column">
                  <b-field label="Birthdate" :label-position="labelPosition">
                    <b-input v-mask="'##/##/####'" v-model="newClient.dependent_4_dob" placeholder="MM/DD/YYYY"></b-input>
                  </b-field>
                </div>
              </div>
              <div class="columns">
                <div class="column">
                  <b-field label="Dependent Name" :label-position="labelPosition">
                      <b-input v-model="newClient.dependent_5_name"></b-input>
                  </b-field>
                </div>
                <div class="column">
                  <b-field label="Birthdate" :label-position="labelPosition">
                    <b-input v-mask="'##/##/####'" v-model="newClient.dependent_5_dob" placeholder="MM/DD/YYYY"></b-input>
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
                <div class="column">
                  <b-field label="Mode of Payment*" :label-position="labelPosition">
                      <b-select placeholder="Select Mode of Payment" expanded v-model="newLoan.loan_mode">
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
                    <b-field label="Co Maker (1)" :label-position="labelPosition">
                        <b-input v-model="newLoan.co_maker"></b-input>
                    </b-field>
                </div>
              </div>
             <div class="columns">
                <div class="column">
                    <b-field label="Co Maker (2)" :label-position="labelPosition">
                        <b-input v-model="newLoan.co_maker_2"></b-input>
                    </b-field>
                </div>
              </div>
              <div class="columns">
                <div class="column">
                  <b-checkbox v-model="newLoan.is_advance">Advanced</b-checkbox>
                </div>
                <div class="column">
                  <label for="">U.D.I</label>
                  <p>{{ calculatedUDI | displayMoney }}</p>
                </div>
              </div>
              <div class="columns">
                <div class="column is-offset-6">
                    <b-field label="Fee Others*" :label-position="labelPosition">
                        <b-input v-model="calculatedOthers"></b-input>
                    </b-field>
                </div>
              </div>
            </section>
            <footer class="modal-card-foot">
              <b-button
                label="Cancel"
                @click="() => {
                  newLoanModal = false;
                  newLoan = {is_advance: true};
                }"/>
              <b-button
                label="Submit"
                type="is-success"
                @click="createLoan()"/>
            </footer>
        </div>
    </b-modal>

    <b-modal v-model="newCAModal" :width="640" scroll="keep">
        <div class="modal-card">
            <header class="modal-card-head">
              <p class="modal-card-title">New Cash Advance</p>
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
            </section>
            <footer class="modal-card-foot">
              <b-button
                label="Cancel"
                @click="() => {
                  newCAModal = false;
                  newLoan = {is_advance: true, add_fee_others: true};
                }"/>
              <b-button
                label="Submit"
                type="is-success"
                @click="createLoan(is_cash_advance = true)"/>
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
    <b-modal v-model="refundModal" :width="640" scroll="keep">
        <div class="modal-card">
            <header class="modal-card-head">
              <p class="modal-card-title">Trying to do a refund</p>
            </header>
            <section class="modal-card-body">
              <div class="columns">
                <div class="column">
                  <label for="">Reference Code:</label>
                  <p class="is-size-4">{{ newRefund.ref_code }}</p>
                </div>
                <div class="column">
                  <label for="">Refundable Amount:</label>
                  <p class="is-size-4">{{ newRefund.amount | displayMoney }}</p>
                </div>
              </div>
              <div class="columns">
                <div class="column">
                    <b-field label="Refund Date" :label-position="labelPosition">
                        <b-input v-mask="'##/##/####'" v-model="newRefund.refund_date" placeholder="MM/DD/YYYY"></b-input>
                    </b-field>
                </div>
              </div>
            </section>
            <footer class="modal-card-foot">
              <b-button
                label="Close"
                @click="() => {
                  refundModal = false
                  newRefund = {}
                }"/>
              <b-button
                label="Refund"
                class="is-success"
                @click="createRefund"/>
            </footer>
        </div>
    </b-modal>
    <!-- End Modals -->

    <!-- Start Sidebar -->
    <b-sidebar
      type="is-light"
      fullheight
      right
      id="loan-sidebar"
      v-model="openSidebar"
      :can-cancel="false"
    >
      <p class="is-size-3 mb-2" v-if="selectedLoan">LOAN {{ selectedLoan.control_number }}</p>
      <div class="columns" v-if="selectedLoan">
        <div class="column">
            <b-button
                label="Close"
                icon-left="times"
                expanded
                @click="()=> {
                  openSidebar=false
                  selectedLoan=null
                }"
                />
        </div>
        <div class="column" v-if="selectedLoan.payments.length == 0">
            <b-button
                label="Delete"
                type="is-danger"
                icon-left="trash"
                expanded
                @click="confirmLoanDelete"
                />
        </div>
      </div>
      <b-tabs type="is-boxed" expanded v-if="selectedLoan">
          <b-tab-item label="Payments">
            <b-table :data="selectedLoan.payments" narrowed striped>
              <b-table-column field="index" label="#" v-slot="props">
                {{ props.index + 1 }}
              </b-table-column>
              <b-table-column field="reference_code" label="Ref Code" v-slot="props">
                {{ props.row.collection.reference_code }}
              </b-table-column>
              <b-table-column field="post_date" label="Date" v-slot="props">
                {{ props.row.collection.post_date | shortDate }}
              </b-table-column>
              <b-table-column field="amount_used" label="Amount" v-slot="props">
                {{ props.row.amount_used | displayMoney }}
              </b-table-column>
              <template #empty>
                <div class="has-text-centered">No Results Found</div>
              </template>
            </b-table>
          </b-tab-item>
          <b-tab-item label="Schedule">
            <b-table :data="selectedLoan.loan_detail" narrowed striped>
              <b-table-column field="index" label="#" v-slot="props">
                {{ props.index + 1 }}
              </b-table-column>
              <b-table-column field="date_payment" label="Due Date" v-slot="props">
                {{ props.row.date_payment | shortDate }}
              </b-table-column>
              <b-table-column field="amount" label="Amount Due" v-slot="props">
                {{ props.row.amount | displayMoney }}
              </b-table-column>
              <b-table-column field="balance" label="Running Balance" v-slot="props">
                {{ props.row.balance | displayMoney }}
              </b-table-column>
              <template #empty>
                <div class="has-text-centered">No Results Found</div>
              </template>
            </b-table>
          </b-tab-item>
          <b-tab-item label="Documents">
            <b-field label="Name" :label-position="labelPosition">
                <b-input v-model="reportDetail.nameOne"></b-input>
            </b-field>
            <b-field label="Name" :label-position="labelPosition">
                <b-input v-model="reportDetail.nameTwo"></b-input>
            </b-field>
            <b-field label="Name" :label-position="labelPosition">
                <b-input v-model="reportDetail.nameThree"></b-input>
            </b-field>
            <b-button @click="printReport('computation')" expanded class="my-1">Computation Report</b-button>
            <b-button @click="printReport('promissory')" expanded class="my-1">Promissory Note</b-button>
            <b-button @click="printReport('disclosure')" expanded class="my-1">Disclosure of Loan</b-button>
          </b-tab-item>
      </b-tabs>
      <div v-if="selectedLoan" class="container-fluid">
        <div class="columns mt-3">
          <div class="column">
            <b-field label="Notes">
                <b-input maxlength="500" type="textarea" v-model="selectedLoan.notes"></b-input>
            </b-field>
          </div>
        </div>
        <div class="columns">
          <div class="column">
            <b-button class="is-success is-pulled-right" @click="saveNotes">Save Notes</b-button>
          </div>
        </div>
      </div>
    </b-sidebar>
    <b-sidebar
      type="is-light"
      fullheight
      right
      id="loan-sidebar"
      v-model="sidebarClient"
      :can-cancel="false"
    >
      <p class="is-size-3 mb-2">Edit Client</p>
      <section class="edit-client" v-if="editingClient">
        <div class="columns">
          <div class="column">
            <b-field label="First Name*" :label-position="labelPosition">
                <b-input v-model="editingClient.first_name"></b-input>
            </b-field>
          </div>
          <div class="column">
              <b-field label="Middle Name" :label-position="labelPosition">
                  <b-input v-model="editingClient.middle_name"></b-input>
              </b-field>
          </div>
          <div class="column">
              <b-field label="Last Name*" :label-position="labelPosition">
                  <b-input v-model="editingClient.last_name"></b-input>
              </b-field>
          </div>
        </div>
        <div class="columns">
          <div class="column is-12">
              <b-field label="Address*" :label-position="labelPosition">
                  <b-input v-model="editingClient.address"></b-input>
              </b-field>
          </div>
        </div>
        <div class="columns">
          <div class="column">
              <b-field label="Contact No" :label-position="labelPosition">
                  <b-input v-model="editingClient.contact_number"></b-input>
              </b-field>
          </div>
          <div class="column">
            <b-field label="Date of Birth*" :label-position="labelPosition">
              <b-input v-mask="'##/##/####'" v-model="editingClient.birth_date" placeholder="MM/DD/YYYY"></b-input>
            </b-field>
          </div>
        </div>
        <div class="columns">
          <div class="column">
            <b-field label="Classification*" :label-position="labelPosition">
                <b-select placeholder="Select Classification" expanded v-model="editingClient.classification">
                    <option
                        v-for="option in classifications"
                        :value="option.value"
                        :key="option.value">
                        {{ option.display }}
                    </option>
                </b-select>
            </b-field>
          </div>
          <div class="column">
            <b-field label="Pensioner Category" :label-position="labelPosition">
                <b-select placeholder="Select Category if Pensioner" expanded v-model="editingClient.pension_type">
                    <option
                        v-for="option in pensionCategories"
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
              <b-field label="Bank Name*" :label-position="labelPosition">
                  <b-input v-model="editingClient.bank_name"></b-input>
              </b-field>
          </div>
          <div class="column">
              <b-field label="Account Number*" :label-position="labelPosition">
                  <b-input v-model="editingClient.account_number"></b-input>
              </b-field>
          </div>
        </div>
        <div class="columns">
          <div class="column">
              <b-field label="Pension/Income Amount*" :label-position="labelPosition">
                  <b-input v-model="editingClient.pension"></b-input>
              </b-field>
          </div>
          <div class="column">
              <b-field label="SSS Number" :label-position="labelPosition">
                  <b-input v-model="editingClient.sss_no"></b-input>
              </b-field>
          </div>
        </div>
        <hr>
        <div class="columns">
          <div class="column">
            <b-field label="Spouse Name" :label-position="labelPosition">
                <b-input v-model="editingClient.spouse_name"></b-input>
            </b-field>
          </div>
        </div>
        <div class="columns">
          <div class="column">
            <b-field label="Spouse Date of Birth" :label-position="labelPosition">
                <b-input v-mask="'##/##/####'" v-model="editingClient.spouse_dob" placeholder="MM/DD/YYYY"></b-input>
            </b-field>
          </div>
          <div class="column">
            <b-field label="Spouse Date of Death" :label-position="labelPosition">
              <b-input v-mask="'##/##/####'" v-model="editingClient.spouse_dod" placeholder="MM/DD/YYYY"></b-input>
            </b-field>
          </div>
        </div>
        <div class="columns">
          <div class="column">
            <b-field label="Dependent Name" :label-position="labelPosition">
                <b-input v-model="editingClient.dependent_1_name"></b-input>
            </b-field>
          </div>
          <div class="column">
            <b-field label="Birthdate" :label-position="labelPosition">
              <b-input v-mask="'##/##/####'" v-model="editingClient.dependent_1_dob" placeholder="MM/DD/YYYY"></b-input>
            </b-field>
          </div>
        </div>
        <div class="columns">
          <div class="column">
            <b-field label="Dependent Name" :label-position="labelPosition">
                <b-input v-model="editingClient.dependent_2_name"></b-input>
            </b-field>
          </div>
          <div class="column">
            <b-field label="Birthdate" :label-position="labelPosition">
              <b-input v-mask="'##/##/####'" v-model="editingClient.dependent_2_dob" placeholder="MM/DD/YYYY"></b-input>
            </b-field>
          </div>
        </div>
        <div class="columns">
          <div class="column">
            <b-field label="Dependent Name" :label-position="labelPosition">
                <b-input v-model="editingClient.dependent_3_name"></b-input>
            </b-field>
          </div>
          <div class="column">
            <b-field label="Birthdate" :label-position="labelPosition">
              <b-input v-mask="'##/##/####'" v-model="editingClient.dependent_3_dob" placeholder="MM/DD/YYYY"></b-input>
            </b-field>
          </div>
        </div>
        <div class="columns">
          <div class="column">
            <b-field label="Dependent Name" :label-position="labelPosition">
                <b-input v-model="editingClient.dependent_4_name"></b-input>
            </b-field>
          </div>
          <div class="column">
            <b-field label="Birthdate" :label-position="labelPosition">
              <b-input v-mask="'##/##/####'" v-model="editingClient.dependent_4_dob" placeholder="MM/DD/YYYY"></b-input>
            </b-field>
          </div>
        </div>
        <div class="columns">
          <div class="column">
            <b-field label="Dependent Name" :label-position="labelPosition">
                <b-input v-model="editingClient.dependent_5_name"></b-input>
            </b-field>
          </div>
          <div class="column">
            <b-field label="Birthdate" :label-position="labelPosition">
              <b-input v-mask="'##/##/####'" v-model="editingClient.dependent_5_dob" placeholder="MM/DD/YYYY"></b-input>
            </b-field>
          </div>
        </div>
        <div class="columns">
          <div class="column">
            <b-button @click="sidebarClient=false" expanded>Cancel</b-button>
          </div>
          <div class="column">
            <b-button class="is-success" @click="patchClient" expanded>Save Changes</b-button>
          </div>
        </div>
      </section>
    </b-sidebar>
    <!-- End Sidebar -->

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
import { createClient, updateClient } from '@/api/client.js'
import { approveLoan, searchLoans, deleteLoan, updateLoan, createLoan } from '@/api/loan.js'
import { createCollection, fetchCollections, deleteCollection } from '@/api/collection.js'
import { createRefund } from '@/api/refund.js'

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
  filters: {
    getAge (dob) {
      return moment().diff(dob, 'years')
    }
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
      newLoan: {is_advance: true, add_fee_others: true, loan_mode: 'monthly'},
      newCA: {is_advance: true, is_cash_advance: true},
      loans: [],
      selectedLoanRows: [],
      newCollection: {},
      collections: [],
      collectionDetails: [],
      newRefund: {},
      reportDetail: {
        nameOne: '',
        nameTwo: '',
        nameThree: ''
      },
      editingClient: {},

      // modals
      newClientModal: false,
      newLoanModal: false,
      newCAModal: false,
      collectionDetailModal : false,
      refundModal: false,

      // sidebar
      openSidebar: false,
      sidebarClient: false,

      //selectOptions
      loanTypes: [
        {value: 'pension', display: 'Pension'},
        {value: 'salary', display: 'Salary'},
      ],
      loan_modes: [
        {value: 'semi_monthly', display: 'Semi Monthly'},
        {value: 'monthly', display: 'Monthly'},
      ],
      classifications: [
        {value: 'pension', display: 'Pensioner'},
        {value: 'salary', display: 'Salary'},
      ],
      pensionCategories: [
        {value: 'RT', display: 'RT'},
        {value: 'SD', display: 'SD'},
        {value: 'SD-ED', display: 'SD-ED'},
        {value: 'RT-SD', display: 'RT-SD'},
        {value: 'GD', display: 'GD'},
        {value: 'EC', display: 'EC'},
        {value: 'SP', display: 'SP'},
        {value: 'ST', display: 'ST'},
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
      ]
    }
  },
  methods: {
    printReport (type) {
        if (type === 'computation') {
            window.open(`${process.env.VUE_APP_API_ENDPOINT_URL}reports/computation_report/${this.selectedLoan.id}/`)
        } else if (type === 'promissory') {
            window.open(`${process.env.VUE_APP_API_ENDPOINT_URL}reports/promissory_report/${this.selectedLoan.id}/?name_one=${this.reportDetail.nameOne}&name_two=${this.reportDetail.nameTwo}&name_three=${this.reportDetail.nameThree}`)
        } else {
            window.open(`${process.env.VUE_APP_API_ENDPOINT_URL}reports/disclosure_of_loan/${this.selectedLoan.id}/`)
        }
    },
    editClient () {
      this.editingClient = {...this.selectedClient}
      this.sidebarClient = true
    },
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
    calculateCollectionTotal (collectionDetails) {
      const details = [...collectionDetails]
      return details.reduce((partial_sum, a) => {
        return partial_sum + parseFloat(a.amount_used)
      }, 0);
    },
    confirmLoanDelete () {
      this.$buefy.dialog.confirm({
          title: 'Are you sure?',
          message: `Deleting Loan ${this.selectedLoan.control_number} will delete the posted net cash out transaction.`,
          cancelText: 'Cancel',
          confirmText: 'Delete',
          type: 'is-danger',
          onConfirm: () => this.trashLoan()
      })
    },
    confirmCollectionDelete (collection) {
      let verbiage = 'Deleting this Collection will also delete associated loan payments.'
      if (collection.is_refunded) {
        verbiage = `${verbiage} Including refunded transaction and will change the outcome of transaction history.`
      }

      this.$buefy.dialog.confirm({
          title: 'Are you sure?',
          message: verbiage,
          cancelText: 'Cancel',
          confirmText: 'Delete',
          type: 'is-danger',
          onConfirm: () => this.trashCollection(collection.id)
      })
    },
    openRefund (collection) {
      this.newRefund = {
        collection: collection.id,
        ref_code: collection.reference_code,
        amount: collection.refundable_amount,
      }

      this.refundModal = true
    },
    async patchClient () {
      try {
        this.isLoading = true

        await updateClient(this.editingClient.id, this.editingClient)

        this.selectedClient = this.editingClient

        this.$buefy.toast.open({
            message: 'Client Updated',
            type: 'is-warning'
        })
      } catch (err) {
        this.$buefy.toast.open({
          message: `Something went wrong: ${err.message}`,
          type: 'is-danger'
        })
      } finally {
        this.isLoading = false
      }
    },
    async saveNotes () {
      try {
        this.isLoading = true

        await updateLoan(this.selectedLoan.id, {notes: this.selectedLoan.notes})
        
        
        this.fetchLoans()
        this.$buefy.toast.open({
            message: 'Loan Notes Saved.',
            type: 'is-warning'
        })
      } catch (err) {
        this.$buefy.toast.open({
          message: `Something went wrong: ${err.message}`,
          type: 'is-danger'
        })
      } finally {
        this.isLoading = false
      }
    },
    async createRefund () {
      try {
        this.isLoading = true

        const refund = {...this.newRefund}
        refund.refund_date = moment(refund.refund_date).format('YYYY-MM-DD')

        await createRefund(refund)

        this.newRefund = {}
        this.refundModal = false
        this.fetchPayments()
        this.$buefy.toast.open({
            message: 'Collection Refunded',
            type: 'is-warning'
        })
      } catch (err) {
        this.$buefy.toast.open({
          message: `Something went wrong: ${err.message}`,
          type: 'is-danger'
        })
      } finally {
        this.isLoading = false
      }
    },
    async trashLoan () {

      try {
        this.isLoading = true
        await deleteLoan(this.selectedLoan.id)
        
        
        this.fetchLoans()
        this.$buefy.toast.open({
            message: 'Loan Deleted Successfully!',
            type: 'is-warning'
        })
        this.selectedLoan = null
        this.openSidebar = false
      } catch (err) {
        this.$buefy.toast.open({
          message: `Something went wrong: ${err.message}`,
          type: 'is-danger'
        })
      } finally {
        this.isLoading = false
      }
    },
    async trashCollection (collectionId) {
      try {
        this.isLoading = true
        await deleteCollection(collectionId)
        
        this.fetchLoans()
        this.fetchPayments()

        this.$buefy.toast.open({
            message: 'Collection was Deleted!',
            type: 'is-warning'
        })
      } catch (err) {
        this.$buefy.toast.open({
          message: `Something went wrong: ${err.message}`,
          type: 'is-danger'
        })
      } finally {
        this.isLoading = false
      }
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
                type: 'is-warning'
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
          type: 'is-warning'
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
    async createLoan (is_cash_advance = false) {
      try {
        this.isLoading = true

        const loan = {...this.newLoan}
        loan.start_payment = moment(loan.start_payment).format('YYYY-MM-DD')
        loan.maturity_date = moment(loan.start_payment).add(loan.term - 1, 'months').format('YYYY-MM-DD')
        loan.principal_amount = parseFloat(loan.principal_amount.replace(/,/g, ''))

        loan.is_cash_advance = is_cash_advance

        const response = await createLoan({
            ...loan,
            client: this.selectedClient.id
        })

        await approveLoan(response.data.id)

        this.$buefy.toast.open({
            message: 'Loan Created Successfully!',
            type: 'is-warning'
        })
        this.newLoanModal = false
        this.newCAModal = false
        this.newLoan = {is_advance: true, add_fee_others: true}
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
    calculatedUDI () {
      if (!!this.newLoan.principal_amount && !!this.newLoan.term && !!this.newLoan.interest) {
        const principalAmount = parseInt(this.newLoan.principal_amount.replace(/,/g, ''))
        const interestRate = this.newLoan.interest * this.newLoan.term
        const udi = (principalAmount * interestRate) / 100
        return udi
      } else {
        return 0
      }
    },
    calculatedOthers: {
      get: function () {
        if (this.calculatedUDI) {
          this.newLoan.fee_others = (0.05 * this.calculatedUDI).toFixed(2)
          return (0.05 * this.calculatedUDI).toFixed(2)
        }
        return 0
      },
      set: function (value) {
        this.newLoan.fee_others = value
      }
    },
    canCreateCollection() {
        if (!!this.newCollection.amount && !!this.newCollection.reference_code && !!this.newCollection.post_date) {
            return false
        }

        return true
    },
    loanTotalRunningBalance () {
      const loans = [...this.loans]
      return loans.reduce((partial_sum, a) => {
        return partial_sum + parseFloat(a.running_balance)
      }, 0);
    },
    totalAmortization () {
      const loans = [...this.loans]
      return loans.reduce((partial_sum, a) => {
        return partial_sum + parseFloat(a.amortization)
      }, 0);
    },
    clientPotentialAP () {
      return this.selectedClient.pension - this.totalAmortization
    },
    loanTotalNetCashOut () {
      const loans = [...this.loans]
      return loans.reduce((partial_sum, a) => {
        return partial_sum + parseFloat(a.net_cash_out)
      }, 0);
    },
  },
  watch: {
    selectedLoanRows(newSelectedLoanRows, _) {
      if (newSelectedLoanRows.length === 0) {
        this.newCollection = {}
      }
    },
    selectedLoan() {
      if (!!this.selectedLoan) {
        this.openSidebar = true
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
    max-height: 665px;
    overflow: scroll;
  }

  #loan-sidebar .sidebar-content {
    width: 30% !important;
    padding: 3em;
    background: #fff;
  }

  #first-section-client {
    border-right: 1px solid #bfbfbf;
  }
</style>