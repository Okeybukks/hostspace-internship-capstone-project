// //
// // A generic load test script provided for example purposes and testing
// //

// import { check, group, sleep } from 'k6'
// import http from 'k6/http'

// const TARGET_URL = __ENV.TEST_TARGET || 'https://httpbin.test.k6.io/'
// const RAMP_TIME = __ENV.RAMP_TIME || '5m'
// const RUN_TIME = __ENV.RUN_TIME || '5m'
// const USER_COUNT = __ENV.USER_COUNT || 30
// const SLEEP = __ENV.SLEEP || 0

// // Very simple ramp up from zero to VUS_MAX over RAMP_TIME, then runs for further RUN_TIME
// export let options = {
//   stages: [
//     { duration: RAMP_TIME, target: USER_COUNT },
//     { duration: RUN_TIME, target: USER_COUNT },
//   ],
// }

// // Totally generic HTTP check
// export default function () {
//   let res = http.get(TARGET_URL)

//   check(res, (r) => r.status === 200)

//   sleep(SLEEP)
// }

import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {

  ext: {
    loadimpact: {
      projectID: '3688226',
      // Test runs with the same name groups test runs together
      name: 'Sample Test'
    }
  },

  stages: [
    { duration: '30s', target: 20 },
    { duration: '1m30s', target: 10 },
    // { duration: '50s', target: 30 },
    // { duration: '40s', target: 45 },
  ],
};

export default function () {
  const res = http.get('https://httpbin.test.k6.io/');
  check(res, { 'status was 200': (r) => r.status == 200 });
  sleep(1);
}