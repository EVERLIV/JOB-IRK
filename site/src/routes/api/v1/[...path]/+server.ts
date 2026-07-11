import type { RequestHandler } from './$types';
import { proxyApiRequest } from '$lib/server/api-proxy';

const handler: RequestHandler = (event) => proxyApiRequest(event);

export const GET = handler;
export const POST = handler;
export const PUT = handler;
export const PATCH = handler;
export const DELETE = handler;
