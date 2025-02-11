import httpRequest from "@/utils/httpRequest"

export const getGoogleOauthUrl = (next: string) => {
    const rootUrl = `https://accounts.google.com/o/oauth2/v2/auth`

    const options = {
        redirect_uri: import.meta.env.VITE_GOOGLE_OAUTH_REDIRECT_URL,
        client_id: import.meta.env.VITE_GOOGLE_OAUTH_CLIENT_ID,
        access_type: "offline",
        response_type: "code",
        scope: [
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
        ].join(" "),
        state: next,
    }

    const qs = new URLSearchParams(options)

    return `${rootUrl}?${qs.toString()}`
}

export const AuthService = {
    api: (additional_headers?: object) =>
        httpRequest({
            baseURL: `${import.meta.env.VITE_FRONTEND_SERVICE_URL}/auth`,
            headers: { ...additional_headers },
        }),

    verifyLogin: function () {
        return this.api().get<null, { isValid: boolean }>("/verify")
    },

    logout: async function () {
        return await this.api().post("/logout")
    },
}
