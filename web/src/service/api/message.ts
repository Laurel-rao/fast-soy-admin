import { request } from '../request';

/** get role list */
export function fetchGetMessageList(params?: Api.SystemManage.RoleSearchParams) {
  return request<Api.SystemManage.MessageList>({
    url: '/system-manage/messages',
    method: 'get',
    params
  });
}

/** add api */
export function fetchAddMessage(data?: Api.Message.MessageCreate) {
  return request<Api.Message.MessageCreate, 'json'>({
    url: '/system-manage/messages',
    method: 'post',
    data
  });
}
