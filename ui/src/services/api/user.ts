import httpRequest from "@/utils/httpRequest"

import { type User } from "@/types/user"

export const UserService = {
    api: (additional_headers?: object) =>
        httpRequest({
            baseURL: `${import.meta.env.VITE_FRONTEND_SERVICE_URL}/users`,
            headers: { ...additional_headers },
        }),

    getUserProfile: async function () {
        return await this.api().get<null, User>("/profile")
    },
}
