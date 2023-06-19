export function jsonToArray(json) {
    const result = [];
    for (const i in json) {
        result.push([i, json[i]])
    }
    return result;
}