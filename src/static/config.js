// static/config.js
/*
 * Copyright 2016 Google Inc. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the
 * License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing permissions and
 * limitations under the License.
 */

var config = {
    apiKey: "AIzaSyBkoNUgQMaHxF-BKmWpqMdkCyWCxVCp9ZQ",
    authDomain: "sagalabs-auth.firebaseapp.com",
    projectId: "sagalabs-auth",
    storageBucket: "sagalabs-auth.appspot.com",
    messagingSenderId: "567952038409",
    appId: "1:567952038409:web:9b0e3d74139e07ecc0b6d8",
    measurementId: "G-NJCNMBZPEX",
};
firebase.initializeApp(config);


// Google OAuth Client ID, needed to support One-tap sign-up.
// Set to null if One-tap sign-up is not supported.
var CLIENT_ID =
    '567952038409-qofpa7i77ni47dchbqf7g9nsifagohj9.apps.googleusercontent.com';
