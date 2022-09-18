#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <pwd.h>
#include <string.h>
#include <stdbool.h>
#include <security/pam_modules.h>
#include <security/pam_ext.h>

const int MAX_ATTEMPTS = 3;

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

	for (int i = 0; i < MAX_ATTEMPTS; ++i) {
		int status = system("python3 /home/raymo/Git/voiceprint-htn/src/cli.py -a");
		printf("status: %d", status);
		if (status == 256) {
			return PAM_SUCCESS;
		}
	}
    return PAM_AUTH_ERR;
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
