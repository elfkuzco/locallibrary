export interface NavigationLink {
    name: string
    path: string
    dropdown?: NavigationLink[]
}
