#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <pwd.h>
#include <string.h>
#include <stdbool.h>
#include <security/pam_modules.h>
#include <security/pam_ext.h>
#include "../bridge/py_identify_bridge.h"

static int send_info_msg(pam_handle_t *pamh, char *msg)
{
	const struct pam_message mymsg = {
		.msg_style = PAM_TEXT_INFO,
		.msg = msg,
	};
	const struct pam_message *msgp = &mymsg;
    const struct pam_conv *pc;
	struct pam_response *resp;
	int r;

    r = pam_get_item(pamh, PAM_CONV, (const void **) &pc);
	if (r != PAM_SUCCESS)
		return 1;

	if (!pc || !pc->conv)
		return 1;

	return pc->conv(1, &msgp, &resp, pc->appdata_ptr);
}

static int send_err_msg(pam_handle_t *pamh, char *msg)
{
	const struct pam_message mymsg = {
		.msg_style = PAM_ERROR_MSG,
		.msg = msg,
	};
	const struct pam_message *msgp = &mymsg;
    const struct pam_conv *pc;
	struct pam_response *resp;
	int r;

    r = pam_get_item(pamh, PAM_CONV, (const void **) &pc);
	if (r != PAM_SUCCESS)
		return 1;

	if (!pc || !pc->conv)
		return 1;

	return pc->conv(1, &msgp, &resp, pc->appdata_ptr);
}

static bool do_identify(pam_handle_t *pamh)
{
	return identify();
}

static int do_auth(pam_handle_t *pamh)
{
	return do_identify(pamh) ? PAM_SUCCESS : PAM_AUTH_ERR;
}

PAM_EXTERN int pam_sm_authenticate(pam_handle_t *pamh, int flags, int argc,
	const char **argv)
{
	const char *rhost = NULL;
	FILE *fd;
	char buf[5];
	const char *username;
	char *homedir;
	struct passwd *passwd;
	int r;

	pam_get_item(pamh, PAM_RHOST, (const void **)(const void*) &rhost);
	if (rhost != NULL && strlen(rhost) > 0) {
		/* remote login (e.g. over SSH) */
		return PAM_AUTHINFO_UNAVAIL;
	}

	r = pam_get_user(pamh, &username, NULL);
	if (r != PAM_SUCCESS)
		return PAM_AUTHINFO_UNAVAIL;

	passwd = getpwnam(username);
	if (!passwd)
		return PAM_AUTHINFO_UNAVAIL;

	homedir = strdup(passwd->pw_dir);

	/* a bit of a hack to make libfprint use the right home dir */


    /* Thomas note */
    /* I guess they are looking for user fingerprint at this "home dir".*/
    /* This can point to where our voice samples/ models are saved? */
	r = setenv("HOME", homedir, 1);
	if (r < 0) {
		free(homedir);
		return PAM_AUTHINFO_UNAVAIL;
	}

	r = do_auth(pamh);
	free(homedir);
	return r;
}

PAM_EXTERN int pam_sm_setcred(pam_handle_t *pamh, int flags, int argc,
	const char **argv)
{
	return PAM_SUCCESS;
}

PAM_EXTERN int pam_sm_chauthtok(pam_handle_t *pamh, int flags, int argc,
	const char **argv)
{
	return PAM_SUCCESS;
}
