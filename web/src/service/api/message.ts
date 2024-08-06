import { request } from '../request';

/** get role list */
export function fetchGetMessageList(params?: Api.SystemManage.RoleSearchParams) {
  return request<Api.SystemManage.MessageList>({
    url: '/system-manage/messages',
    method: 'get',
    params
  });
}
