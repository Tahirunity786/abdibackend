$(document).ready(function () {
   $(".switchPatient").click(function () {
      $(".signpatient-form").removeClass("display-none");
      $(".signpatient-form").addClass("display-block");
      $(".signdoctor-form").addClass("display-none");
      $(".signadmin-form").addClass("display-none");
      $(".switchPatient").addClass("btnActive");
      $(".switchDoctor").removeClass("btnActive");
      $(".switchAdmin").removeClass("btnActive");
      $(".content").css("margin-top", "50px");
   });

   $(".switchDoctor").click(function () {
      $(".signdoctor-form")
         .removeClass("display-none")
         .addClass("display-block");
      $(".content").css("margin-top", "100px");
      $(".signpatient-form, .signadmin-form").addClass("display-none");
      $(".switchDoctor").addClass("btnActive");
      $(".switchPatient, .switchAdmin").removeClass("btnActive");
   });

   $(".switchAdmin").click(function () {
      $(".signadmin-form").removeClass("display-none");
      $(".signadmin-form").addClass("display-block");
      $(".signpatient-form").addClass("display-none");
      $(".signdoctor-form").addClass("display-none");
      $(".switchAdmin").addClass("btnActive");
      $(".switchPatient").removeClass("btnActive");
      $(".switchDoctor").removeClass("btnActive");
      $(".content").css("margin-top", "100px");
   });


   $("#signinPassIcon").click(function () {
      $("#signinPassIcon i").toggleClass("fa-eye fa-eye-slash");

      $($("#signinPassIcon").siblings()[1]).attr("type", function (index, attr) {
         return attr == "password" ? "text" : "password";
      })
   });

   $("#signupPassIcon").click(function () {
      $("#signupPassIcon i").toggleClass("fa-eye fa-eye-slash");

      $($("#signupPassIcon").siblings()[1]).attr("type", function (index, attr) {
         return attr == "password" ? "text" : "password";
      })
   });




   $("#signinPassIcon2").click(function () {
      $("#signinPassIcon2 i").toggleClass("fa-eye fa-eye-slash");

      $($("#signinPassIcon2").siblings()[1]).attr("type", function (index, attr) {
         return attr == "password" ? "text" : "password";
      })
   });

   $("#signupPassIcon2").click(function () {
      $("#signupPassIcon2 i").toggleClass("fa-eye fa-eye-slash");

      $($("#signupPassIcon2").siblings()[1]).attr("type", function (index, attr) {
         return attr == "password" ? "text" : "password";
      })
   });
});





document.addEventListener("DOMContentLoaded", function () {
   var accountLink = document.getElementById('account');
   var profileLink = document.getElementById('profile');
   var bedReservements = document.getElementById('bed-reserve');
   var doctorAppointments = document.getElementById('dc-appoint');
   var contactLink = document.getElementById('cont');

   accountLink.addEventListener('click', function () {
      showSection('account-setting');
   });
   profileLink.addEventListener('click', function () {
      showSection('profile-setting');
   });
   bedReservements.addEventListener('click', function () {
      showSection('bed-reservements');
   });
   doctorAppointments.addEventListener('click', function () {
      showSection('doc-appointments');
   });
   contactLink.addEventListener('click', function () {
      showSection('contact');
   });

   function showSection(sectionId) {
      var sections = ['account-setting', 'profile-setting', 'bed-reservements','doc-appointments', 'contact'];

      sections.forEach(function (section) {
         var element = document.getElementById(section);
         if (section === sectionId) {
            element.style.display = 'block';
         } else {
            element.style.display = 'none';
         }
      });
   }
});


$(document).ready(function () {
   $(".switchSignin").click(function(){
      $(".signin-form").removeClass("display-none");
      $(".signin-form").addClass("display-block");
      $(".signup-form").addClass("display-none");
      $(".switchSignin").addClass("btnActive");
      $(".switchSignup").removeClass("btnActive");
   });
   
   $(".switchSignup").click(function(){
      $(".signup-form").removeClass("display-none");
      $(".signup-form").addClass("display-block");
      $(".signin-form").addClass("display-none");
      $(".switchSignup").addClass("btnActive");
      $(".switchSignin").removeClass("btnActive");
   });


   $("#signinPassIcon").click(function(){
      $("#signinPassIcon i").toggleClass("fa-eye fa-eye-slash");

      $($("#signinPassIcon").siblings()[1]).attr("type", function(index, attr){
         return attr == "password" ? "text" : "password";
      })
   });
   
   $("#signupPassIcon").click(function(){
      $("#signupPassIcon i").toggleClass("fa-eye fa-eye-slash");

      $($("#signupPassIcon").siblings()[1]).attr("type", function(index, attr){
         return attr == "password" ? "text" : "password";
      })
   });
});