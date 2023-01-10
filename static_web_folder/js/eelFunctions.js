const GetBackups = () => {
    return eel.GetBackups()()
}
const SaveWorld = (name, description) => {
    return eel.SaveWorld(name, description)()
}
const LoadWorld = (id) => {
    return eel.LoadWorld(id)()
}

const RemoveBackup = (id) => {
    return eel.RemoveBackup(id)()
}
const ModifyBackup = (id, name = null, description = null) => {
    return eel.ModifyBackup(id, name, description)()
}