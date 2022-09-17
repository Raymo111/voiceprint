#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <pwd.h>
#include <string.h>
#include <stdbool.h>
#include <security/pam_modules.h>
#include <security/pam_ext.h>

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
		return;

	if (!pc || !pc->conv)
		return;

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
		return;

	if (!pc || !pc->conv)
		return;

	return pc->conv(1, &msgp, &resp, pc->appdata_ptr);
}

/* fprint artifact
static const char *fingerstr(enum fp_finger finger)
{
	const char *names[] = {
		[LEFT_THUMB] = "left thumb",
		[LEFT_INDEX] = "left index",
		[LEFT_MIDDLE] = "left middle",
		[LEFT_RING] = "left ring",
		[LEFT_LITTLE] = "left little",
		[RIGHT_THUMB] = "right thumb",
		[RIGHT_INDEX] = "right index",
		[RIGHT_MIDDLE] = "right middle",
		[RIGHT_RING] = "right ring",
		[RIGHT_LITTLE] = "right little",
	};
	if (finger < LEFT_THUMB || finger > RIGHT_LITTLE)
		return "UNKNOWN";
	return names[finger];
}


static struct fp_print_data **find_dev_and_prints(struct fp_dscv_dev **ddevs,
	struct fp_dscv_print **prints, struct fp_dscv_dev **_ddev, enum fp_finger **fingers)
{
	int i = 0, j = 0, err;
	struct fp_dscv_print *print;
	struct fp_dscv_dev *ddev = NULL;
	uint16_t driver_id, driver_id_cur;
	size_t prints_count = 0;
	struct fp_print_data **gallery;

	while (print = prints[i++]) {
		if (!ddev) {
			ddev = fp_dscv_dev_for_dscv_print(ddevs, print);
			driver_id = fp_dscv_print_get_driver_id(print);
			*_ddev = ddev;
		}
		if (ddev)
		{
		    driver_id_cur = fp_dscv_print_get_driver_id(print);
		    if (driver_id_cur == driver_id) {
			    prints_count++;
		    }
		}
	}
	
	if (prints_count == 0) {
	    return NULL;
	}
	
	gallery = malloc(sizeof(*gallery) * (prints_count + 1));
	if (gallery == NULL) {
	    return NULL;
	}
	gallery[prints_count] = NULL;
	*fingers = malloc(sizeof(*fingers) * (prints_count));
	if (*fingers == NULL) {
	    free(gallery);
	    return NULL;
	}
	
	i = 0, j = 0;
	while (print = prints[i++]) {
		driver_id_cur = fp_dscv_print_get_driver_id(print);
		if (driver_id_cur == driver_id) {
			err = fp_print_data_from_dscv_print(print, & (gallery[j]));
			if (err != 0) {
			    gallery[j] = NULL;
			    break;
			}
			(*fingers)[j] = fp_dscv_print_get_finger(print);
			j++;
		}
	}
	
	return gallery;
}

*/

static bool do_identify(pam_handle_t *pamh)
{
	return true;
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

