import { varchar, serial, pgTable, integer, date, numeric } from "drizzle-orm/pg-core";
import { users } from "../users/model";

export const userStatistic = pgTable('userstatistic',
{
    id: serial('id').primaryKey(),
    user: integer('user_id').references(() => users.id, {onDelete: 'cascade'}).notNull(),
    sendMessagesCount: integer('sendMessagesCount'),
    receivedMessagesCount:  integer('receivedMessagesCount'),
    recipientCounts: integer('recipientCounts'),
    bccCount: integer('bccCount'),
    ccCount: integer('ccCount'),
    //daysBetweenReceivedAndRead: ArrayField(integer),
    repliedMessagesCount: integer('repliedMessagesCount'),
    sentCharactersCount: integer('sentCharactersCount'),
    messagesOutsideWorkingHours: integer('messagesOutsideWorkingHours'),
    receivedToSentRatio: numeric('receivedToSentRatio'),
    bytesReceivedToSentRatio: numeric('bytesReceivedToSentRatio'),
    messagesWithQuestionAndNoReply: integer('messagesWithQuestionAndNoReply'),
    readMessagesMoreThan4Hours: integer('readMessagesMoreThan4Hours'),
    startInterval: date('startInterval'),
    endInterval: date('endInterval')
})
    