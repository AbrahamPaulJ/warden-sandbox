export function log(msg: string) {
  if (process.env.DEBUG) console.log(msg);
}
