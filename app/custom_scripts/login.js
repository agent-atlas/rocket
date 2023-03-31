Accounts.validateLoginAttempt(function(attempt) {
    var userAgent = attempt.userAgent;
    var isAdmin = attempt.user && Roles.userIsInRole(attempt.user._id, 'admin');
    var isMobileApp = userAgent && userAgent.browser && userAgent.browser.name === 'RocketChatMobile';
  
    if (isMobileApp && !isAdmin) {
      throw new Meteor.Error(403, 'Mobile app login is not allowed');
    }
  
    return true;
  });